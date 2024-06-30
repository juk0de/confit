import pytest
import tempfile
from pathlib import Path
from import_confit import confit


def test_apply_file_cp():
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
            install_files=[(str(src_file), "testfile.txt")]
        )

        # Perform the apply
        group.apply(verbose=True)

        # Check if the file was copied correctly
        dst_file = dst_dir / "testfile.txt"
        assert dst_file.exists()
        with open(dst_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_apply_file_rsync():
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
        assert "rsync" in confit.rsync, "Test failed because of missing 'rsync'"

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_file), "testfile.txt")]
        )

        # Perform the apply
        group.apply(verbose=True)

        # Check if the file was copied correctly
        dst_file = dst_dir / "testfile.txt"
        assert dst_file.exists()
        with open(dst_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_apply_directory_cp():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create subdirectories and files in the source directory
        sub_dir = src_dir / "subdir"
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
            install_files=[(str(sub_dir), "subdir")]
        )

        # Perform the apply
        group.apply(verbose=True)

        # Check if the directory and files were copied correctly
        dst_sub_dir = dst_dir / "subdir"
        assert dst_sub_dir.exists() and dst_sub_dir.is_dir()

        dst_file1 = dst_sub_dir / "file1.txt"
        dst_file2 = dst_sub_dir / "file2.txt"

        assert dst_file1.exists()
        assert dst_file2.exists()

        with open(dst_file1, "r") as f:
            content = f.read()
            assert content == "This is file 1."
        with open(dst_file2, "r") as f:
            content = f.read()
            assert content == "This is file 2."


def test_apply_directory_rsync():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create subdirectories and files in the source directory
        sub_dir = src_dir / "subdir"
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
            install_files=[(str(sub_dir), "subdir")]
        )

        # Perform the apply
        group.apply(verbose=True)

        # Check if the directory and files were copied correctly
        dst_sub_dir = dst_dir / "subdir"
        assert dst_sub_dir.exists() and dst_sub_dir.is_dir()

        dst_file1 = dst_sub_dir / "file1.txt"
        dst_file2 = dst_sub_dir / "file2.txt"

        assert dst_file1.exists()
        assert dst_file2.exists()

        with open(dst_file1, "r") as f:
            content = f.read()
            assert content == "This is file 1."
        with open(dst_file2, "r") as f:
            content = f.read()
            assert content == "This is file 2."


if __name__ == "__main__":
    pytest.main()
