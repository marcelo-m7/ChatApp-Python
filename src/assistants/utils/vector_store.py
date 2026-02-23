"""Legacy module retained as a disabled shim.

Use `assistants.utils.archive.vector_store` only for historical reference.
"""

import warnings

warnings.warn(
    "assistants.utils.vector_store is legacy/experimental and disabled. "
    "Use active runtime modules documented in assistants.utils/README.md.",
    DeprecationWarning,
    stacklevel=2,
)


def get_vector_store(*args, **kwargs):
    raise RuntimeError(
        "assistants.utils.vector_store has been disabled and moved to "
        "assistants.utils.archive.vector_store"
    )
