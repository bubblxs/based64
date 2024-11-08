import os
import sys
import hashlib
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from based64 import FILE_EXT, encode_file_to_base64, decode_base64_file

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

class Stat: # <---- omg just like c
    def __init__(self, file_path):
        self.filename = os.path.basename(file_path)
        self.file_path = file_path
        self.size = os.path.getsize(file_path)
        self.md5 = get_file_hash(file_path)

class TestFileEncoding(unittest.TestCase):
    def setUp(self):
        self.working_dir = os.path.dirname(os.path.realpath(__file__))
        self.files = os.listdir(os.path.join(self.working_dir, "files"))
        self.test_files = {}

        for f in self.files:
            file_path = os.path.join(self.working_dir, "files", f)
            st = Stat(file_path)
            self.test_files[f] = st

    def test_file_encoding(self):
        for filename, file_obj in self.test_files.items():
            og_file_path = os.path.join(self.working_dir, "files", filename)
            expected_hash = file_obj.md5

            encode_file_to_base64(og_file_path)

            os.remove(og_file_path)

            decoded_file_path = f"{og_file_path}.{FILE_EXT}"
            decode_base64_file(decoded_file_path)

            current_md5 = get_file_hash(og_file_path)

            os.remove(decoded_file_path)

            self.assertEqual(expected_hash, current_md5, f"hashes dont match {filename}: expected '{expected_hash}' got '{current_md5}'.")

if __name__ == "__main__":
    unittest.main()