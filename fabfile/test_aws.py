import unittest
import itertools
from aws import AwsManager
from fabfile import CONF_PATH


class TestAwsManager(unittest.TestCase):

    def test_constructor(self):
        filtered = [True, False]
        allow_terminated = [True, False]
        conf_path = [None, CONF_PATH]
        for f, a, c in itertools.product(filtered, allow_terminated, conf_path):
            try:
                m = AwsManager(c, filtered=f, allow_terminated=a)
                self.assertIsInstance(m._cfg, dict)
            except TypeError:
                if c is None:
                    pass
                else:
                    raise

    def test_launch_instance_with_wait(self):
        m = AwsManager(conf_path=CONF_PATH)
        # print('launching 1')
        i1 = m.launch_new_instance('_foo_test_1')
        self.assertEqual(i1.tags['Name'], '_foo_test_1')
        # print('launching 2')
        i2 = m.launch_new_instance('_foo_test_2')
        # print('instances launched')
        try:
            instances = m.get_instances()
            self.assertEqual(len(instances), 2)
            self.assertEqual(set([i.update() for i in instances.values()]), set(['running']))
        finally:
            i1.terminate()
            i2.terminate()
        self.assertEqual(m.get_instances(), {})

    def test_launch_instance_without_wait(self):
        m = AwsManager(conf_path=CONF_PATH)
        i1 = m.launch_new_instance('_foo_test_1', wait=False)
        try:
            self.assertNotEqual(i1.update(), 'running')
        finally:
            i1.terminate()
        self.assertEqual(m.get_instances(), {})

    def test_name_must_be_unique(self):
        m = AwsManager(conf_path=CONF_PATH)
        self.assertEqual(m.get_instances(), {})
        try:
            i1 = m.launch_new_instance('_foo_test_4', wait=True)
            i2 = m.launch_new_instance('_foo_test_4', wait=True)
        finally:
            try:
                i1.terminate()
                i2.terminate()
            except UnboundLocalError:
                pass
