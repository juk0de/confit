import pytest
import tempfile
from pathlib import Path
from import_confit import confit


def test_diff_no_difference():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create a sample file in both source and destination directories
        src_file = src_dir / "testfile.txt"
        dst_file = dst_dir / "testfile.txt"
        content = "This is a test file."
        with open(src_file, "w") as f:
            f.write(content)
        with open(dst_file, "w") as f:
            f.write(content)

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_file), "testfile.txt")]
        )

        # Perform the diff
        assert not group.diff(verbose=True)


def test_diff_with_difference():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create a sample file in both source and destination directories with different content
        src_file = src_dir / "testfile.txt"
        dst_file = dst_dir / "testfile.txt"
        with open(src_file, "w") as f:
            f.write("This is a test file.")
        with open(dst_file, "w") as f:
            f.write("This is a different test file.")

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_file), "testfile.txt")]
        )

        # Perform the diff
        assert group.diff(verbose=True)


def test_diff_file_missing_in_dest():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source directory
        src_dir = tempdir_path / "src"
        src_dir.mkdir()

        # Create a sample file in the source directory
        src_file = src_dir / "testfile.txt"
        with open(src_file, "w") as f:
            f.write("This is a test file.")

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=tempdir_path / "dst",
            install_files=[(str(src_file), "testfile.txt")]
        )

        # Perform the diff
        assert group.diff(verbose=True)


def test_diff_directory():
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

        # Create corresponding subdirectories and files in the destination directory with different content
        dst_sub_dir = dst_dir / "subdir"
        dst_sub_dir.mkdir()
        dst_file1 = dst_sub_dir / "file1.txt"
        dst_file2 = dst_sub_dir / "file2.txt"
        with open(dst_file1, "w") as f:
            f.write("This is a different file 1.")
        with open(dst_file2, "w") as f:
            f.write("This is a different file 2.")

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir), "src")]
        )

        # Perform the diff
        assert group.diff(verbose=True)


if __name__ == "__main__":
    pytest.main()
