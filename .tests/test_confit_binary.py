import tempfile
import shutil
import subprocess
from pathlib import Path
import pytest


@pytest.fixture(scope="module")
def confit_path():
    path = Path(__file__).resolve().parent.parent / 'confit'
    if not path.exists():
        pytest.skip(f"confit binary not found at {path}")
    return path


def test_confit_help(confit_path):
    result = subprocess.run([confit_path, '--help'], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage: confit" in result.stdout


def test_confit_no_args(confit_path):
    result = subprocess.run([confit_path], capture_output=True, text=True)
    assert result.returncode != 0
    assert "the following arguments are required" in result.stderr


def test_confit_groups(confit_path):
    config_content = """
    groups:
      testgroup:
        dest: /tmp/dest
        install_files:
          - [src.txt, dst.txt]
    """
    with tempfile.TemporaryDirectory() as tempdir:
        config_file = Path(tempdir) / ".conf.it"
        with open(config_file, "w") as f:
            f.write(config_content)
        confit_binary = Path(tempdir) / "confit"
        shutil.copy(confit_path, confit_binary)
        result = subprocess.run([confit_binary, 'groups'], capture_output=True, text=True, cwd=tempdir)
        assert result.returncode == 0
        assert "testgroup" in result.stdout
