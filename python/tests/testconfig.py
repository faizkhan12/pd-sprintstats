import unittest
import os
from lib.configuration import parse_config
from tempfile import NamedTemporaryFile
from ConfigParser import SafeConfigParser

class TestConfigurationModule(unittest.TestCase):

    def setUp(self):
        self.files = []
        for n in range(4):
            temp_config = NamedTemporaryFile(delete=False)
            self.files.append(temp_config.name)
            parser = SafeConfigParser()
            parser.read(temp_config)
            parser.set('DEFAULT', 'index', str(n))
            parser.write(temp_config)


    def tearDown(self):
        for tempfile in self.files:
            os.remove(tempfile)


    def test_configs_loaded_in_order(self):
        for n in range(4):
            files = self.files[0:n+1]
            config = parse_config(None, files)
            index = config.get('index')
            self.assertEqual(int(index), n)


    def test_config_returns_default_points(self):
        config = parse_config(None, self.files)
        self.assertTrue('default_points' in config)
        self.assertEqual(config['default_points'], 0)


    def test_config_expands_homedir_path(self):
        f = NamedTemporaryFile(delete=False, dir=os.path.expanduser('~'))
        basename = os.path.basename(f.name)
        userpath = os.path.join('~', basename)
        parser = SafeConfigParser()
        parser.read(f)
        parser.set('DEFAULT', 'homedir', 'very_yes')
        parser.write(f)
        f.close()
        config = parse_config(None, [userpath])
        homedir = config.get('homedir')
        self.assertEqual(homedir, 'very_yes')
        f.close()
        os.remove(f.name)

