import pytest
import tempfile
from pathlib import Path
from import_confit import confit, ConfitError
from unittest.mock import patch


def create_config_file(content, tempdir):
    config_file = Path(tempdir) / ".conf.it"
    with open(config_file, "w") as f:
        f.write(content)
    return config_file


def test_load_config_valid():
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            dest: /tmp/dest
            files:
              - [src.txt, dst.txt]
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "testgroup" in groups
        assert groups["testgroup"].dest == Path("/tmp/dest")


def test_load_config_invalid():
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            dest: /tmp/dest
            files:
              - [src.txt, dst.txt
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        with pytest.raises(ConfitError):
            confit.load_config()


def test_load_config_missing_file():
    confit.confit_files = ["/nonexistent/.conf.it"]
    with pytest.raises(ConfitError):
        confit.load_config()


@patch('import_confit.confit.get_hostname', return_value='testhost')
def test_load_config_with_host_filter(mock_get_hostname):
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            dest: /tmp/dest
            files:
              - [src.txt, dst.txt]
            host: testhost
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "testgroup" in groups
        assert groups["testgroup"].dest == Path("/tmp/dest")


@patch('import_confit.confit.get_hostname', return_value='wronghost')
def test_install_with_host_filter_no_match(mock_get_hostname):
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            dest: /tmp/dest
            files:
              - [src.txt, dst.txt]
            host: testhost
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "testgroup" not in groups
