from pathlib import Path

# Repository-aware paths for assistant knowledge assets.
SRC_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_ROOT = SRC_ROOT / "assistants" / "data" / "knowledge"
FLET_KNOWLEDGE_DIR = KNOWLEDGE_ROOT / "flet"
WEB_SCRAPER_JSON_DIR = FLET_KNOWLEDGE_DIR / "__extracted_code"

# Existing corpus files used by the local TextLoader mode.
SITE_DATA_LIGHT_FILE = WEB_SCRAPER_JSON_DIR / "docs_controls_image.json"
SITE_DATA_FILE = WEB_SCRAPER_JSON_DIR / "docs_getting-started_flet-controls.json"
DOCS_PICKLE_FILE = FLET_KNOWLEDGE_DIR / "docs.pickle"
