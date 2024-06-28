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
