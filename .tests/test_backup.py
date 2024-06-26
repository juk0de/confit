import pytest
import tempfile
from pathlib import Path
from import_confit import confit
from datetime import datetime
import time


def test_backup_file():
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

        # Get the modification time of the file
        mod_time = dst_file.stat().st_mtime

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "testfile.txt"), "testfile.txt")]
        )

        # Perform the backup
        group.backup()

        # Check if the backup file was created correctly
        timestamp = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d-%H:%M:%S')
        backup_file = dst_dir / f"testfile.txt.ba.{timestamp}"
        assert backup_file.exists()
        with open(backup_file, "r") as f:
            content = f.read()
            assert content == "This is a test file."


def test_backup_multiple_files():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create source and destination directories
        src_dir = tempdir_path / "src"
        dst_dir = tempdir_path / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()

        # Create multiple sample files in the destination directory
        dst_file1 = dst_dir / "testfile1.txt"
        dst_file2 = dst_dir / "testfile2.txt"
        with open(dst_file1, "w") as f:
            f.write("This is test file 1.")
        with open(dst_file2, "w") as f:
            f.write("This is test file 2.")

        # Get the modification times of the files
        mod_time1 = dst_file1.stat().st_mtime
        mod_time2 = dst_file2.stat().st_mtime

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "testfile1.txt"), "testfile1.txt"),
                           (str(src_dir / "testfile2.txt"), "testfile2.txt")]
        )

        # Perform the backup
        group.backup()

        # Check if the backup files were created correctly
        timestamp1 = datetime.fromtimestamp(mod_time1).strftime('%Y-%m-%d-%H:%M:%S')
        timestamp2 = datetime.fromtimestamp(mod_time2).strftime('%Y-%m-%d-%H:%M:%S')
        backup_file1 = dst_dir / f"testfile1.txt.ba.{timestamp1}"
        backup_file2 = dst_dir / f"testfile2.txt.ba.{timestamp2}"
        assert backup_file1.exists()
        assert backup_file2.exists()
        with open(backup_file1, "r") as f:
            content = f.read()
            assert content == "This is test file 1."
        with open(backup_file2, "r") as f:
            content = f.read()
            assert content == "This is test file 2."


def test_backup_max_backups():
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

        # Define the ConfGroup with max_backups set to 3
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "testfile.txt"), "testfile.txt")],
            max_backups=3
        )

        # Perform the backup multiple times
        for _ in range(5):
            group.backup()
            # re-create the file since it's renamed during backup
            with open(dst_file, "w") as f:
                f.write("This is a test file.")
            time.sleep(1)  # Ensure the timestamp changes

        # Check if only 3 backup files are kept
        backups = sorted(dst_dir.glob("testfile.txt.ba.*"), key=lambda p: p.stat().st_mtime)
        assert len(backups) == 3


def test_backup_directory():
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

        # Get the modification times of the directory
        mod_time = sub_dir.stat().st_mtime

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dst_dir,
            install_files=[(str(src_dir / "subdir"), "subdir")]
        )

        # Perform the backup
        group.backup()

        # Check if the backup files were created correctly
        timestamp = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d-%H:%M:%S')
        backup_dir = dst_dir / f"subdir.ba.{timestamp}"
        assert backup_dir.exists()
        # Check if 'backup_dir' contains the same files as 'sub_dir'
        for src_file in sub_dir.rglob('*'):
            backup_file = backup_dir / src_file.relative_to(sub_dir)
            assert backup_file.exists()
            if src_file.is_file():
                with open(src_file, "r") as src_f, open(backup_file, "r") as backup_f:
                    assert src_f.read() == backup_f.read()


if __name__ == "__main__":
    pytest.main()
