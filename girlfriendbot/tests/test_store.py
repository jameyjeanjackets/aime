import os
import unittest
import tempfile
import json
from bot.store import ChatStore


class TestChatStore(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, 'test_chat.db')
        self.store = ChatStore(db_path=self.db_path)
        self.user_id = 'u_test'
        self.session_id = 's1'

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_and_get(self):
        self.store.add_message(self.user_id, self.session_id, 'user', 'hello')
        self.store.add_message(self.user_id, self.session_id, 'assistant', 'hi')
        conv = self.store.get_conversation(self.user_id, self.session_id)
        self.assertEqual(len(conv), 2)
        self.assertEqual(conv[0]['role'], 'user')
        self.assertEqual(conv[0]['content'], 'hello')
        self.assertEqual(conv[1]['role'], 'assistant')

    def test_export(self):
        self.store.add_message(self.user_id, self.session_id, 'user', 'hey')
        out_path = os.path.join(self.tmpdir.name, 'out.json')
        res = self.store.export_conversation(self.user_id, self.session_id, path=out_path)
        self.assertTrue(os.path.exists(res))
        with open(res, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]['content'], 'hey')


if __name__ == '__main__':
    unittest.main()
