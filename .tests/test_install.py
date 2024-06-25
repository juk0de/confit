from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
import pytest
import tempfile
from pathlib import Path
import sys
# Add the directory containing the `confit` module to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
spec = spec_from_loader("confit", SourceFileLoader("confit", "confit"))
if not spec:
    raise RuntimeError("Failed to load 'confit' module! Please run tests from the repository root.")
confit = module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(confit)
sys.modules['confit'] = confit


def test_install():
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


if __name__ == "__main__":
    pytest.main()
