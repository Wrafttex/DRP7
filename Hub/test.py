import unittest
from mqttTools import puplish, subscribe

class TestStringMethods(unittest.TestCase):

    def test_publish_connect(self):
        self.pubClient = puplish.connect_mqtt()
        self.assertIs(self.pubClient, puplish.mqtt_client.Client)

    def test_publish_publish(self):
        self.assertTrue(puplish.publish(self.pubClient))

    def test_publish_run(self):
        self.assertTrue(puplish.run(self.pubClient))

    def test_subscribe_connect(self):
        self.subClient = subscribe.connect_mqtt()
        self.assertIs(self.subClient, subscribe.mqtt_client.Client)

    def test_subscribe_subscribe(self):
        self.assertTrue(puplish.publish(self.subClient))

    def test_subscribe_run(self):
        self.assertTrue(puplish.run(self.subClient))

    def test_x(self):
        pass

    # def test_fail(self):
    #     self.assertFalse(True)

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()