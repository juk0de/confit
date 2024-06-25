import pytest
import tempfile
from pathlib import Path
from import_confit import confit


def test_install_cp():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create a sample file in the source directory
        src_file = src_dir / "testfile.txt"
        with open(src_file, "w") as f:
            f.write("This is a test file.")

        # disable rsync for this test
        confit.rsync = None

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            files=[(str(src_file), "testfile.txt")]
        )

        # Perform the install
        group.install(force=False)

        # Check if the file was copied correctly
        dst_file = dst_dir / "testfile.txt"
        assert dst_file.exists()
        with open(dst_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_install_rsync():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create a sample file in the source directory
        src_file = src_dir / "testfile.txt"
        with open(src_file, "w") as f:
            f.write("This is a test file.")

        # enable rsync for this test
        confit.rsync = confit.find_rsync()
        assert "rsync" in confit.rsync

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            files=[(str(src_file), "testfile.txt")]
        )

        # Perform the install
        group.install(force=False)

        # Check if the file was copied correctly
        dst_file = dst_dir / "testfile.txt"
        assert dst_file.exists()
        with open(dst_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


if __name__ == "__main__":
    pytest.main()
