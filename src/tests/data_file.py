import unittest
from pathlib import Path
from config import DATA_PATH


class DataFile(unittest.TestCase):

    def setUp(self):
        self.data_path = Path(DATA_PATH)

    def test_data_path_exists(self):
        self.assertTrue(self.data_path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

