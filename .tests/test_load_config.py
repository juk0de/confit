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
            name: test
            dest: /tmp/dest
            install_files:
              - [src.txt, dst.txt]
            check_binaries:
              - [binary1, description1]
            post_install_cmds:
              - [command1, /tmp]
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "test" in groups
        assert groups["test"].dest == Path("/tmp/dest")
        assert groups["test"].check_binaries == [("binary1", "description1")]
        assert groups["test"].post_install_cmds == [("command1", "/tmp")]


def test_load_config_sync_files_omitted():
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            name: test
            dest: /tmp/dest
            install_files:
              - [src.txt, dst.txt]
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "test" in groups
        assert groups["test"].sync_files == groups["test"].install_files


def test_load_config_sync_files_empty():
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            name: test
            dest: /tmp/dest
            install_files:
              - [src.txt, dst.txt]
            sync_files: []
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "test" in groups
        assert groups["test"].sync_files == []


def test_load_config_sync_files_specified():
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            name: test
            dest: /tmp/dest
            install_files:
              - [src.txt, dst.txt]
            sync_files:
              - [sync_src.txt, sync_dst.txt]
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "test" in groups
        assert groups["test"].sync_files == [("sync_src.txt", "sync_dst.txt")]


def test_load_config_invalid_syntax():
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            name: test
            dest: /tmp/dest
            install_files:
              - [src.txt, dst.txt
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        with pytest.raises(ConfitError):
            confit.load_config()


def test_load_config_invalid_mapping():
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

        config_content = f"""
        groups:
          testgroup:
            name: test
            dest: /tmp/dest
            install_files:
              - [{src_file}, {dst_dir}]
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        with pytest.raises(ConfitError, match="Invalid mapping in group 'test'"):
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
            name: test
            dest: /tmp/dest
            install_files:
              - [src.txt, dst.txt]
            hosts:
              - testhost
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "test" in groups
        assert groups["test"].dest == Path("/tmp/dest")


@patch('import_confit.confit.get_hostname', return_value='wronghost')
def test_load_config_with_host_filter_no_match(mock_get_hostname):
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          testgroup:
            name: test
            dest: /tmp/dest
            install_files:
              - [src.txt, dst.txt]
            hosts:
              - testhost
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "test" not in groups


def test_load_config_duplicate_group_names():
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          group1:
            name: duplicate
            dest: /tmp/dest1
            install_files:
              - [src1.txt, dst1.txt]
          group2:
            name: duplicate
            dest: /tmp/dest2
            install_files:
              - [src2.txt, dst2.txt]
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        with pytest.raises(ConfitError, match="Found two groups with wih identical name 'duplicate'"):
            confit.load_config()


@patch('import_confit.confit.get_hostname', return_value='testhost')
def test_load_config_duplicate_group_names_with_different_hosts(mock_get_hostname):
    with tempfile.TemporaryDirectory() as tempdir:
        config_content = """
        groups:
          group1:
            name: duplicate
            dest: /tmp/dest1
            install_files:
              - [src1.txt, dst1.txt]
            hosts:
              - testhost
          group2:
            name: duplicate
            dest: /tmp/dest2
            install_files:
              - [src2.txt, dst2.txt]
            hosts:
              - otherhost
        """
        create_config_file(config_content, tempdir)
        confit.confit_files = [str(Path(tempdir) / ".conf.it")]
        config, groups = confit.load_config()
        assert "duplicate" in groups
        assert groups["duplicate"].dest == Path("/tmp/dest1")
