import unittest

from contact_book import ContactBook


class ContactBookTests(unittest.TestCase):
    def setUp(self):
        self.contact_book = ContactBook()
        self.contact_book.add_contact("Alice", "555-0100", "alice@example.com")

    def test_add_and_search_contact(self):
        self.assertEqual(
            self.contact_book.search_contacts("ali"),
            {"Alice": {"phone": "555-0100", "email": "alice@example.com"}},
        )

    def test_update_contact(self):
        self.contact_book.update_contact("Alice", phone="555-0101")

        self.assertEqual(self.contact_book.contacts["Alice"]["phone"], "555-0101")
        self.assertEqual(
            self.contact_book.contacts["Alice"]["email"], "alice@example.com"
        )

    def test_delete_contact(self):
        self.contact_book.delete_contact("Alice")

        self.assertEqual(self.contact_book.contacts, {})

    def test_duplicate_and_missing_contacts_raise_errors(self):
        with self.assertRaises(ValueError):
            self.contact_book.add_contact("Alice", "555-0102")
        with self.assertRaises(KeyError):
            self.contact_book.delete_contact("Bob")


if __name__ == "__main__":
    unittest.main()