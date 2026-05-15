from __future__ import annotations

import logging
import os
import pickle
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DocusaurusLoader, TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings

from assistants.utils.manager_tools import ManagerTools as mt

logger = logging.getLogger(__name__)


class DataStore:
    """
    Manage document loading and vector store creation for the chat application.
    """

    WEB = "web"
    LOCAL = "text"
    PICKLE = "pickle"
    # Backward-compatibility alias
    PICKEL = PICKLE

    SITE_URL = "https://kobu.agency/"

    _BASE_DIR = Path(__file__).resolve().parents[1]
    _KNOWLEDGE_DIR = _BASE_DIR / "data" / "knowledge"
    _DATA_STORE_DIR = _KNOWLEDGE_DIR / "data_store_files" / "default"

    site_datas_light = str(_DATA_STORE_DIR / "site_datas_light.txt")
    site_datas = str(_DATA_STORE_DIR / "site_datas.txt")

    LOCAL_PATH = site_datas
    docs_pickle_path = str(_DATA_STORE_DIR / "docs.pickle")
    origin = LOCAL

    @classmethod
    def get_vector_store(
        cls,
        origin_preference: str = PICKLE,
        oringin_preference: str | None = None,
    ) -> FAISS:
        """
        Retrieve or build a vector store.

        Args:
            origin_preference: Preferred source (`pickle`, `web`, or `text`).
            oringin_preference: Backward-compatible misspelled parameter name.
        """
        selected_preference = oringin_preference or origin_preference

        try:
            if selected_preference == cls.PICKLE:
                vector_store = cls.get_doc_from_pickle()
                logger.info("Vector store loaded from pickle source")
            elif selected_preference in [cls.WEB, cls.LOCAL]:
                logger.info("Creating vector store from origin", extra={"origin": selected_preference})
                vector_store = cls.create_db_critical(selected_preference)
            else:
                raise ValueError(f"Invalid origin preference: {selected_preference}")

            logger.info("Vector store obtained successfully")
            return vector_store

        except Exception:
            logger.exception("Error obtaining vector store. Falling back to default origin")
            return cls.create_db_critical(cls.origin)

    @classmethod
    @mt.debugger_exception_decorator
    def get_doc_from_pickle(cls) -> FAISS:
        """
        Build a vector store from documents loaded via pickle cache.
        """
        docs = cls._load_or_create_pickled_docs()
        embedding = cls._load_embeddings()
        return cls._build_vector_store(docs, embedding)

    @classmethod
    # Backward-compatibility alias
    def get_doc_from_pickel(cls) -> FAISS:
        return cls.get_doc_from_pickle()

    @classmethod
    @mt.debugger_exception_decorator
    def prepare_doc_to_be_pickeled(cls) -> list:
        """
        Prepare documents to be pickled.
        """
        docs = cls._load_documents(cls.origin, chunk_size=750, chunk_overlap=30)
        logger.info("Prepared documents for pickle", extra={"count": len(docs), "origin": cls.origin})
        return docs

    @classmethod
    @mt.debugger_exception_decorator
    def pickle_handler(cls, parameter: list) -> list:
        """
        Persist and return documents in pickle format.
        """
        pickle_path = Path(cls.docs_pickle_path)
        pickle_path.parent.mkdir(parents=True, exist_ok=True)

        if not pickle_path.exists():
            with pickle_path.open("wb") as file_handler:
                pickle.dump(parameter, file_handler)
            logger.info("Created pickle file", extra={"path": str(pickle_path)})
        else:
            logger.info("Pickle file already exists", extra={"path": str(pickle_path)})

        with pickle_path.open("rb") as file_handler:
            loaded_variable = pickle.load(file_handler)

        logger.info("Loaded variable from pickle", extra={"path": str(pickle_path)})
        return loaded_variable

    @classmethod
    def create_db_critical(cls, origin: str = WEB) -> FAISS:
        """
        Create a vector store from web or local documents.
        """
        docs = cls._load_documents(origin, chunk_size=550, chunk_overlap=30)
        embedding = cls._load_embeddings()
        return cls._build_vector_store(docs, embedding)

    @classmethod
    def _load_or_create_pickled_docs(cls) -> list:
        pickle_path = Path(cls.docs_pickle_path)

        if pickle_path.exists():
            with pickle_path.open("rb") as file_handler:
                docs = pickle.load(file_handler)
            logger.info("Loaded docs from pickle", extra={"path": str(pickle_path), "count": len(docs)})
            return docs

        docs = cls.prepare_doc_to_be_pickeled()
        return cls.pickle_handler(docs)

    @classmethod
    def _get_loader(cls, origin: str):
        if origin == cls.WEB:
            return DocusaurusLoader(url=cls.SITE_URL)

        if origin == cls.LOCAL:
            if not os.path.exists(cls.LOCAL_PATH):
                raise FileNotFoundError(f"Local knowledge file not found: {cls.LOCAL_PATH}")
            return TextLoader(file_path=cls.LOCAL_PATH, encoding="utf-8")

        raise ValueError(f"Invalid origin: {origin}")

    @classmethod
    def _load_documents(cls, origin: str, chunk_size: int, chunk_overlap: int) -> list:
        loader = cls._get_loader(origin)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        split_docs = splitter.split_documents(docs)
        logger.info(
            "Loaded and split documents",
            extra={
                "origin": origin,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "count": len(split_docs),
            },
        )
        return split_docs

    @staticmethod
    def _load_embeddings() -> OpenAIEmbeddings:
        logger.info("Loading embeddings")
        return OpenAIEmbeddings()

    @staticmethod
    def _build_vector_store(docs: list, embedding: OpenAIEmbeddings) -> FAISS:
        logger.info("Building vector store", extra={"count": len(docs)})
        return FAISS.from_documents(docs, embedding=embedding)
