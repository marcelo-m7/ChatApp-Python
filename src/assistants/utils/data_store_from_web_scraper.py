"""Legacy module retained as a disabled shim.

Use `assistants.utils.archive.data_store_from_web_scraper` only for historical reference.
"""

import warnings

warnings.warn(
    "assistants.utils.data_store_from_web_scraper is legacy/experimental and disabled. "
    "Use active runtime modules documented in assistants.utils/README.md.",
    DeprecationWarning,
    stacklevel=2,
)


def get_vector_store(*args, **kwargs):
    raise RuntimeError(
        "assistants.utils.data_store_from_web_scraper has been disabled and moved to "
        "assistants.utils.archive.data_store_from_web_scraper"
    )
