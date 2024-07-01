from unittest.mock import patch
from import_confit import confit
from pathlib import Path


def test_check_all_binaries_found():
    group = confit.ConfGroup(
        name="testgroup",
        dest=Path("/tmp/dest"),
        install_files=[],
        check_binaries=[("binary1", "description1"), ("binary2", "description2")]
    )

    with patch("shutil.which", side_effect=["/usr/bin/binary1", "/usr/bin/binary2"]):
        result = group.check()
        assert result is True


def test_check_some_binaries_not_found():
    group = confit.ConfGroup(
        name="testgroup",
        dest=Path("/tmp/dest"),
        install_files=[],
        check_binaries=[("binary1", "description1"), ("binary2", "description2")]
    )

    with patch("shutil.which", side_effect=["/usr/bin/binary1", None]):
        result = group.check()
        assert result is False


def test_check_no_binaries_to_check():
    group = confit.ConfGroup(
        name="testgroup",
        dest=Path("/tmp/dest"),
        install_files=[],
        check_binaries=[]
    )

    result = group.check()
    assert result is True
