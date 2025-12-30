import logging
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from photobooth import USERDATA_PATH

logger = logging.getLogger(name=None)


def test_main_instance_create_dirs_permission_error():
    from photobooth import _create_basic_folders

    with patch.object(os, "makedirs", side_effect=RuntimeError("effect: failed creating folder")):
        # emulate write access issue and ensure an exception is received to make the app fail starting.
        with pytest.raises(RuntimeError):
            _create_basic_folders()


def test_main_instance_create_dirs_permission_errorreraised_stops_starting_app():
    with patch.object(os, "makedirs", side_effect=PermissionError("effect: failed creating folder")):
        # emulate write access issue and ensure an exception is received to make the app fail starting.
        with pytest.raises(RuntimeError):
            __import__("photobooth.__init__")


def test_init_error_if_demoassets_is_no_symlink():
    target = Path(USERDATA_PATH, "demoassets")
    target.unlink(missing_ok=True)

    target.touch()
    assert target.is_file()

    with pytest.raises(RuntimeError):
        __import__("photobooth.__init__")

    target.unlink(missing_ok=False)


def test_init_userdata_after_init_there_is_demoassets_symlink():
    def is_junction(path: Path) -> bool:
        """Check if path is a junction on Windows (compatible with Python 3.11)"""
        if os.name != "nt":
            return False
        # For Python 3.12+, use the built-in method
        if hasattr(path, "is_junction"):
            return path.is_junction()
        # For Python 3.11, check using file attributes
        import stat

        try:
            return path.exists() and bool(path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        except (OSError, AttributeError):
            # Fallback: use os.path.islink
            return os.path.islink(path)

    target = Path(USERDATA_PATH, "demoassets")
    target.unlink(missing_ok=True)

    # starting the app creates the symlink
    __import__("photobooth.__init__")

    if os.name == "nt":
        assert is_junction(target)
    else:
        assert target.is_symlink()
