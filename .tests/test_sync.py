import pytest
import tempfile
from pathlib import Path
from import_confit import confit


def test_sync_file_cp():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create a sample file in the destination directory
        dst_file = dst_dir / "testfile.txt"
        with open(dst_file, "w") as f:
            f.write("This is a test file.")

        # disable rsync for this test
        confit.rsync = None

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "testfile.txt"), "testfile.txt")]
        )

        # Perform the sync
        group.synchronize()

        # Check if the file was copied correctly
        src_file = src_dir / "testfile.txt"
        assert src_file.exists()
        with open(src_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_sync_file_rsync():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create a sample file in the destination directory
        dst_file = dst_dir / "testfile.txt"
        with open(dst_file, "w") as f:
            f.write("This is a test file.")

        # enable rsync for this test
        confit.rsync = confit.find_rsync()
        assert "rsync" in confit.rsync, "Test failed because of missing 'rsync'"

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "testfile.txt"), "testfile.txt")]
        )

        # Perform the sync
        group.synchronize()

        # Check if the file was copied correctly
        src_file = src_dir / "testfile.txt"
        assert src_file.exists()
        with open(src_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_sync_directory_cp():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create subdirectories and files in the destination directory
        sub_dir = dst_dir / "subdir"
        sub_dir.mkdir()
        file1 = sub_dir / "file1.txt"
        file2 = sub_dir / "file2.txt"
        with open(file1, "w") as f:
            f.write("This is file 1.")
        with open(file2, "w") as f:
            f.write("This is file 2.")

        # disable rsync for this test
        confit.rsync = None

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "subdir"), "subdir")]
        )

        # Perform the sync
        group.synchronize()

        # Check if the directory and files were copied correctly
        src_sub_dir = src_dir / "subdir"
        assert src_sub_dir.exists() and src_sub_dir.is_dir()

        src_file1 = src_sub_dir / "file1.txt"
        src_file2 = src_sub_dir / "file2.txt"

        assert src_file1.exists()
        assert src_file2.exists()

        with open(src_file1, "r") as f:
            content = f.read()
            assert content == "This is file 1."
        with open(src_file2, "r") as f:
            content = f.read()
            assert content == "This is file 2."


def test_sync_directory_rsync():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create subdirectories and files in the destination directory
        sub_dir = dst_dir / "subdir"
        sub_dir.mkdir()
        file1 = sub_dir / "file1.txt"
        file2 = sub_dir / "file2.txt"
        with open(file1, "w") as f:
            f.write("This is file 1.")
        with open(file2, "w") as f:
            f.write("This is file 2.")

        # enable rsync for this test
        confit.rsync = confit.find_rsync()
        assert "rsync" in confit.rsync, "Test failed because of missing 'rsync'"

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "subdir"), "subdir")]
        )

        # Perform the sync
        group.synchronize()

        # Check if the directory and files were copied correctly
        src_sub_dir = src_dir / "subdir"
        assert src_sub_dir.exists() and src_sub_dir.is_dir()

        src_file1 = src_sub_dir / "file1.txt"
        src_file2 = src_sub_dir / "file2.txt"

        assert src_file1.exists()
        assert src_file2.exists()

        with open(src_file1, "r") as f:
            content = f.read()
            assert content == "This is file 1."
        with open(src_file2, "r") as f:
            content = f.read()
            assert content == "This is file 2."


def test_sync_file_missing_in_dest():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source directory
        src_dir = tempdir_path / "src"
        src_dir.mkdir()

        # Create a sample file in the source directory
        src_file = src_dir / "testfile.txt"
        with open(src_file, "w") as f:
            f.write("This is a test file.")

        # disable rsync for this test
        confit.rsync = None

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=tempdir_path / "dst",
            install_files=[(str(src_file), "testfile.txt")]
        )

        # Perform the sync
        group.synchronize()

        # Check if the file was not deleted in the source directory
        assert src_file.exists()
        with open(src_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


if __name__ == "__main__":
    pytest.main()
