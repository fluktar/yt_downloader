import unittest
import os
from paths import save_user_paths, load_user_paths
from fileops import delete_file
from ytdownloader import check_free_space
from stats import load_stats, save_stats, add_to_stats


class TestPaths(unittest.TestCase):
    def setUp(self):
        # Prepare a test file for user paths
        self.test_file = "test_user_paths.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_user_paths(self):
        # Test saving and loading user paths to/from a JSON file
        paths = ["/tmp/test1", "/tmp/test2"]
        save_user_paths(paths, self.test_file)
        loaded = load_user_paths(self.test_file)
        self.assertEqual(paths, loaded)


class TestFileOps(unittest.TestCase):
    def setUp(self):
        # Create a test file for file operations
        self.test_file = "test_fileops.txt"
        with open(self.test_file, "w") as f:
            f.write("test")

    def tearDown(self):
        # Remove the test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_delete_file(self):
        # Test deleting a file
        self.assertTrue(os.path.exists(self.test_file))
        delete_file(self.test_file)
        self.assertFalse(os.path.exists(self.test_file))


class TestHelpers(unittest.TestCase):
    def test_check_free_space(self):
        # Test checking free space in a directory
        ok, free = check_free_space(".")
        self.assertTrue(ok)
        self.assertIsInstance(free, int)


class TestStats(unittest.TestCase):
    def setUp(self):
        # Prepare a test stats file
        self.stats_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_stats.log"
        )
        self._orig_stats_file = None
        # Patch STATS_FILE in stats module
        import stats

        self._orig_stats_file = stats.STATS_FILE
        stats.STATS_FILE = self.stats_file

    def tearDown(self):
        # Restore original STATS_FILE and remove test stats file
        import stats

        stats.STATS_FILE = self._orig_stats_file
        if os.path.exists(self.stats_file):
            os.remove(self.stats_file)

    def test_save_and_load_stats(self):
        # Test saving and loading stats (MB)
        save_stats(123.45)
        loaded = load_stats()
        self.assertAlmostEqual(loaded, 123.45, places=2)

    def test_add_to_stats(self):
        # Test adding bytes to stats and updating the total
        save_stats(0)
        total = add_to_stats(1048576)  # 1 MB
        self.assertAlmostEqual(total, 1.0, places=2)
        total = add_to_stats(1048576)  # +1 MB
        self.assertAlmostEqual(total, 2.0, places=2)


if __name__ == "__main__":
    unittest.main()
