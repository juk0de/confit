import pytest
from import_confit import confit
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_load_config():
    with patch('import_confit.confit.load_config') as mock_load:
        mock_load.return_value = (
            {
                'groups': {
                    'group1': {
                        'dest': '/tmp/dest1',
                        'install_files': [['src1.txt', 'dst1.txt']]
                    },
                    'group2': {
                        'dest': '/tmp/dest2',
                        'install_files': [['src2.txt', 'dst2.txt']]
                    }
                }
            },
            {
                'group1': MagicMock(),
                'group2': MagicMock()
            }
        )
        yield mock_load


def test_groups_cmd_all_groups(capsys, mock_load_config):
    confit.config, confit.groups = confit.load_config()
    args = MagicMock()
    args.group = None
    confit.groups_cmd(args)
    captured = capsys.readouterr()
    assert "group1" in captured.out
    assert "group2" in captured.out


def test_groups_cmd_specific_group(capsys, mock_load_config):
    confit.config, confit.groups = confit.load_config()
    args = MagicMock()
    args.group = 'group1'
    confit.groups_cmd(args)
    captured = capsys.readouterr()
    assert "group1" in captured.out
    assert "dest: /tmp/dest1" in captured.out
    assert "install_files" in captured.out


def test_groups_cmd_nonexistent_group(capsys, mock_load_config):
    confit.config, confit.groups = confit.load_config()
    args = MagicMock()
    args.group = 'nonexistent'
    confit.groups_cmd(args)
    captured = capsys.readouterr()
    assert "Group 'nonexistent' not found." in captured.out
