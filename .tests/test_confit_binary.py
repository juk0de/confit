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


def test_confit_wrong_directory(confit_path):
    with tempfile.TemporaryDirectory() as tempdir:
        result = subprocess.run([confit_path, '--help'], capture_output=True, text=True, cwd=tempdir)
        print(result.stdout)
        assert result.returncode != 0
        assert "Error: 'confit' must be run from:" in result.stderr


def test_confit_help(confit_path):
    result = subprocess.run([confit_path, '--help'], capture_output=True, text=True)
    print(result.stdout)
    assert result.returncode == 0
    assert "usage: confit" in result.stdout


def test_confit_no_args(confit_path):
    result = subprocess.run([confit_path], capture_output=True, text=True)
    print(result.stdout)
    assert result.returncode != 0
    assert "the following arguments are required" in result.stderr


def test_confit_groups(confit_path):
    config_content = """
    groups:
      testgroup:
        name: foo
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
        # print the group list
        result = subprocess.run([confit_binary, 'groups'], capture_output=True, text=True, cwd=tempdir)
        print(result.stdout)
        assert result.returncode == 0
        assert "foo" in result.stdout


def test_confit_groups_with_group(confit_path):
    config_content = """
    groups:
      testgroup:
        name: foo
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
        # print the complete group data
        result = subprocess.run([confit_binary, 'groups', 'foo'], capture_output=True, text=True, cwd=tempdir)
        print(result.stdout)
        assert result.returncode == 0
        assert "/tmp/dest" in result.stdout


def test_confit_groups_with_non_existing_group(confit_path):
    config_content = """
    groups:
      testgroup:
        name: foo
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
        # print the complete group data
        result = subprocess.run([confit_binary, 'groups', 'bla'], capture_output=True, text=True, cwd=tempdir)
        print(result.stdout)
        assert result.returncode == 1


def test_confit_diff_differences(confit_path):
    config_content = """
    groups:
      testgroup:
        name: test
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

        # Create source and destination files
        src_file = Path(tempdir) / "src.txt"
        dst_file = Path("/tmp/dest/dst.txt")
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        src_file.write_text("source content")
        dst_file.write_text("destination content")

        result = subprocess.run([confit_binary, 'diff', '--no-pager', 'test'], capture_output=True, text=True, cwd=tempdir)
        print(result.stdout)
        assert result.returncode == 1
        assert "diff" in result.stdout


def test_confit_diff_no_differences(confit_path):
    config_content = """
    groups:
      testgroup:
        name: test
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

        # Create source and destination files
        src_file = Path(tempdir) / "src.txt"
        dst_file = Path("/tmp/dest/dst.txt")
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        src_file.write_text("content")
        dst_file.write_text("content")

        result = subprocess.run([confit_binary, 'diff', '--no-pager', 'test'], capture_output=True, text=True, cwd=tempdir)
        print(result.stdout)
        assert result.returncode == 0
        assert "diff" in result.stdout
