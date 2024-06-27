import pytest
import tempfile
from pathlib import Path
from import_confit import confit


def test_install_file_cp():
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

        # Perform the install
        group.install(force=False)

        # Check if the file was copied correctly
        dst_file = dst_dir / "testfile.txt"
        assert dst_file.exists()
        with open(dst_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_install_file_rsync():
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

        # Perform the install
        group.install(force=False)

        # Check if the file was copied correctly
        dst_file = dst_dir / "testfile.txt"
        assert dst_file.exists()
        with open(dst_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_install_if_dest_file_exists_cp():
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

        # Create a file in the destination directory to simulate existing file
        dst_file = dst_dir / "testfile.txt"
        with open(dst_file, "w") as f:
            f.write("This file already exists.")

        # disable rsync for this test
        confit.rsync = None

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_file), "testfile.txt")]
        )

        # Perform the install and expect an exception
        with pytest.raises(confit.ConfitError, match="Destination '.*' exists .*"):
            group.install(force=False)

        # repeat with force flag
        group.install(force=True)

        # check that the destination file has been overwritten
        # -> the content is different, which makes the check easy
        assert dst_file.exists()
        with open(dst_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_install_directory_cp():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create subdirectories and files in the source directory
        sub_dir_empty = src_dir / "empty_subdir"
        sub_dir_with_files = src_dir / "subdir_with_files"
        sub_dir_empty.mkdir()
        sub_dir_with_files.mkdir()

        file1 = sub_dir_with_files / "file1.txt"
        file2 = sub_dir_with_files / "file2.txt"
        file3 = sub_dir_with_files / "file3.txt"

        with open(file1, "w") as f:
            f.write("This is file 1.")
        with open(file2, "w") as f:
            f.write("This is file 2.")
        with open(file3, "w") as f:
            f.write("This is file 3.")

        # disable rsync for this test
        confit.rsync = None

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir), "src")]
        )

        # Perform the install
        group.install(force=False)

        # Check if the directory and files were copied correctly
        dst_sub_dir_empty = dst_dir / "src" / "empty_subdir"
        dst_sub_dir_with_files = dst_dir / "src" / "subdir_with_files"
        assert dst_sub_dir_empty.exists() and dst_sub_dir_empty.is_dir()
        assert dst_sub_dir_with_files.exists() and dst_sub_dir_with_files.is_dir()

        dst_file1 = dst_sub_dir_with_files / "file1.txt"
        dst_file2 = dst_sub_dir_with_files / "file2.txt"
        dst_file3 = dst_sub_dir_with_files / "file3.txt"

        assert dst_file1.exists()
        assert dst_file2.exists()
        assert dst_file3.exists()

        with open(dst_file1, "r") as f:
            content = f.read()
            assert content == "This is file 1."
        with open(dst_file2, "r") as f:
            content = f.read()
            assert content == "This is file 2."
        with open(dst_file3, "r") as f:
            content = f.read()
            assert content == "This is file 3."


def test_install_directory_rsync():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create subdirectories and files in the source directory
        sub_dir_empty = src_dir / "empty_subdir"
        sub_dir_with_files = src_dir / "subdir_with_files"
        sub_dir_empty.mkdir()
        sub_dir_with_files.mkdir()

        file1 = sub_dir_with_files / "file1.txt"
        file2 = sub_dir_with_files / "file2.txt"
        file3 = sub_dir_with_files / "file3.txt"

        with open(file1, "w") as f:
            f.write("This is file 1.")
        with open(file2, "w") as f:
            f.write("This is file 2.")
        with open(file3, "w") as f:
            f.write("This is file 3.")

        # enable rsync for this test
        confit.rsync = confit.find_rsync()
        assert "rsync" in confit.rsync, "Test failed because of missing 'rsync'"

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir), "src")]
        )

        # Perform the install
        group.install(force=False)

        # Check if the directory and files were copied correctly
        dst_sub_dir_empty = dst_dir / "src" / "empty_subdir"
        dst_sub_dir_with_files = dst_dir / "src" / "subdir_with_files"
        assert dst_sub_dir_empty.exists() and dst_sub_dir_empty.is_dir()
        assert dst_sub_dir_with_files.exists() and dst_sub_dir_with_files.is_dir()

        dst_file1 = dst_sub_dir_with_files / "file1.txt"
        dst_file2 = dst_sub_dir_with_files / "file2.txt"
        dst_file3 = dst_sub_dir_with_files / "file3.txt"

        assert dst_file1.exists()
        assert dst_file2.exists()
        assert dst_file3.exists()

        with open(dst_file1, "r") as f:
            content = f.read()
            assert content == "This is file 1."
        with open(dst_file2, "r") as f:
            content = f.read()
            assert content == "This is file 2."
        with open(dst_file3, "r") as f:
            content = f.read()
            assert content == "This is file 3."


def test_install_if_dest_directory_exists_cp():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create subdirectories and files in the source directory
        sub_dir_empty = src_dir / "empty_subdir"
        sub_dir_with_files = src_dir / "subdir_with_files"
        sub_dir_empty.mkdir()
        sub_dir_with_files.mkdir()

        file1 = sub_dir_with_files / "file1.txt"
        file2 = sub_dir_with_files / "file2.txt"
        file3 = sub_dir_with_files / "file3.txt"

        with open(file1, "w") as f:
            f.write("This is file 1.")
        with open(file2, "w") as f:
            f.write("This is file 2.")
        with open(file3, "w") as f:
            f.write("This is file 3.")

        # Create a directory in the destination to simulate existing directory
        dst_sub_dir_empty = dst_dir / "src" / "empty_subdir"
        dst_sub_dir_with_files = dst_dir / "src" / "subdir_with_files"
        dst_sub_dir_empty.mkdir(parents=True)
        dst_sub_dir_with_files.mkdir(parents=True)

        # disable rsync for this test
        confit.rsync = None

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir), "src")]
        )

        # Perform the install and expect an exception
        with pytest.raises(confit.ConfitError, match="Destination '.*' exists .*"):
            group.install(force=False)

        # repeat with force flag
        group.install(force=True)

        # Check if the directory and files were copied correctly
        assert dst_sub_dir_empty.exists() and dst_sub_dir_empty.is_dir()
        assert dst_sub_dir_with_files.exists() and dst_sub_dir_with_files.is_dir()

        dst_file1 = dst_sub_dir_with_files / "file1.txt"
        dst_file2 = dst_sub_dir_with_files / "file2.txt"
        dst_file3 = dst_sub_dir_with_files / "file3.txt"

        assert dst_file1.exists()
        assert dst_file2.exists()
        assert dst_file3.exists()

        with open(dst_file1, "r") as f:
            content = f.read()
            assert content == "This is file 1."
        with open(dst_file2, "r") as f:
            content = f.read()
            assert content == "This is file 2."
        with open(dst_file3, "r") as f:
            content = f.read()
            assert content == "This is file 3."


if __name__ == "__main__":
    pytest.main()
