import unittest
import os
from paths import save_user_paths, load_user_paths
from fileops import delete_file
from ytdownloader import check_free_space


class TestPaths(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_user_paths.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_user_paths(self):
        paths = ["/tmp/test1", "/tmp/test2"]
        save_user_paths(paths, self.test_file)
        loaded = load_user_paths(self.test_file)
        self.assertEqual(paths, loaded)


class TestFileOps(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_fileops.txt"
        with open(self.test_file, "w") as f:
            f.write("test")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_delete_file(self):
        self.assertTrue(os.path.exists(self.test_file))
        delete_file(self.test_file)
        self.assertFalse(os.path.exists(self.test_file))


class TestHelpers(unittest.TestCase):
    def test_check_free_space(self):
        # Sprawdź na katalogu, który na pewno istnieje
        ok, free = check_free_space(".")
        self.assertTrue(ok)
        self.assertIsInstance(free, int)


if __name__ == "__main__":
    unittest.main()
