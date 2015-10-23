from ..utils import (Color, create_zdict_db_if_not_exists,
                     create_zdict_dir_if_not_exists,
                     import_readline)

from pytest import raises
from unittest.mock import patch


class TestColor:
    def setup_method(self, method):
        self.color = Color()

    def teardown_method(self, method):
        del self.color

    @patch('zdict.utils.sys.stdout.isatty', return_value=True)
    def test_format_in_tty(self, isatty):
        assert '\33[31;1mtest\33[0m' == self.color.format('test', 'lred')
        assert '\33[31mtest\33[0m' == self.color.format('test', 'red')
        assert '  \33[31mtest\33[0m' == self.color.format('test', 'red', indent=2)
        assert isatty.called

    @patch('zdict.utils.sys.stdout.isatty', return_value=False)
    def test_format_not_tty(self, isatty):
        assert '  test' == self.color.format('test', 'red', indent=2)
        assert isatty.called

    def test_format_none(self):
        assert self.color.format(None) is None

    def test_attribute(self):
        self.color.red = '\33[31m'
        self.color.lred = '\33[31;1m'
        with raises(AttributeError):
            self.color.test


@patch('zdict.utils.constants')
@patch('os.mkdir')
@patch('os.path.isdir', return_value=False)
def test_create_zdict_dir_if_not_exists(mkdir, isdir, constants):
    constants.BASE_DIR = '/mock'
    create_zdict_dir_if_not_exists()

    isdir.assert_called_with('/mock')
    mkdir.assert_called_with('/mock')


@patch('builtins.open')
@patch('zdict.utils.constants')
@patch('os.path.exists', return_value=False)
def test_create_zdict_db_if_not_exists(exists, constants, open):
    constants.DB_FILE = '/mock'
    create_zdict_db_if_not_exists()

    exists.assert_called_with('/mock')
    assert open.called


@patch('zdict.utils.sys')
def test_platform_readline(sys):
    '''
    Check the imported readline module on different platforms
    '''
    sys.platform = 'linux'
    readline = import_readline()
    assert readline.__name__ == 'readline'

    sys.platform = 'darwin'
    readline = import_readline()
    if sys.version_info < (3, 5):
        assert readline.__name__ == 'gnureadline'
    else:
        assert readline.__name__ == 'readline'

    sys.platform = 'foo'
    readline = import_readline()
    assert readline.__name__ == 'readline'
