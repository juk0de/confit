import pytest
import tempfile
from pathlib import Path
from import_confit import confit
import subprocess


def test_configure():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create a destination directory
        dest_dir = tempdir_path / "dest"
        dest_dir.mkdir()

        # Create a sample script to be executed
        script_file = dest_dir / "script.sh"
        with open(script_file, "w") as f:
            f.write("#!/bin/bash\necho 'Hello, World!' > output.txt\n")
        script_file.chmod(0o755)

        # Define the ConfGroup
        group = confit.ConfGroup(
            name="testgroup",
            dest=dest_dir,
            install_files=[],
            config_cmds=[("./script.sh", ".")]
        )

        # Perform the configure
        group.configure(verbose=True)

        # Check if the script was executed correctly
        output_file = dest_dir / "output.txt"
        assert output_file.exists()
        with open(output_file, "r") as f:
            content = f.read()
            assert content == "Hello, World!\n"


def test_configure_with_nonexistent_script():
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)

        # Create a destination directory
        dest_dir = tempdir_path / "dest"
        dest_dir.mkdir()

        # Define the ConfGroup with a nonexistent script
        group = confit.ConfGroup(
            name="testgroup",
            dest=dest_dir,
            install_files=[],
            config_cmds=[("./nonexistent.sh", ".")]
        )

        # Perform the configure and expect an exception
        with pytest.raises(subprocess.CalledProcessError):
            group.configure(verbose=True)


if __name__ == "__main__":
    pytest.main()
