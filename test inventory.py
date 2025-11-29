# tests/test_inventory.py
import unittest
from pathlib import Path
import tempfile
import json

from library_manager.inventory import LibraryInventory

class TestLibraryInventory(unittest.TestCase):
    def setUp(self):
        # Create a temp file for storage so tests don't touch real data
        self.tmpfile = Path(tempfile.mktemp(suffix=".json"))
        # Ensure file exists with empty list
        self.tmpfile.write_text("[]", encoding="utf-8")
        self.inv = LibraryInventory(storage_path=self.tmpfile)

    def tearDown(self):
        if self.tmpfile.exists():
            self.tmpfile.unlink()

    def test_add_and_search(self):
        book = self.inv.add_book("Test Book", "Author A", "ISBN123")
        self.assertEqual(book.title, "Test Book")
        found = self.inv.search_by_isbn("ISBN123")
        self.assertIsNotNone(found)
        self.assertEqual(found.author, "Author A")

    def test_issue_and_return(self):
        self.inv.add_book("T", "A", "I1")
        self.assertTrue(self.inv.issue_book("I1"))
        # issuing again should return False (already issued)
        self.assertFalse(self.inv.issue_book("I1"))
        self.assertTrue(self.inv.return_book("I1"))
        # returning again should return False (already available)
        self.assertFalse(self.inv.return_book("I1"))

if _name_ == "_main_":
    unittest.main()
