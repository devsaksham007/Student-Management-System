"""A simple contact book implemented with a dictionary."""


class ContactBook:
    """Store contacts by name and provide CRUD operations."""

    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone, email=""):
        """Add a contact, raising ValueError when the name already exists."""
        name = self._clean_name(name)
        if name in self.contacts:
            raise ValueError("A contact with that name already exists.")

        self.contacts[name] = {"phone": phone.strip(), "email": email.strip()}

    def search_contacts(self, query):
        """Return contacts whose names contain the query, case-insensitively."""
        query = query.strip().lower()
        return {
            name: details
            for name, details in self.contacts.items()
            if query in name.lower()
        }

    def update_contact(self, name, phone=None, email=None):
        """Update the supplied fields of an existing contact."""
        name = self._clean_name(name)
        if name not in self.contacts:
            raise KeyError("Contact not found.")

        if phone is not None:
            self.contacts[name]["phone"] = phone.strip()
        if email is not None:
            self.contacts[name]["email"] = email.strip()

    def delete_contact(self, name):
        """Delete an existing contact."""
        name = self._clean_name(name)
        if name not in self.contacts:
            raise KeyError("Contact not found.")
        del self.contacts[name]

    @staticmethod
    def _clean_name(name):
        name = name.strip()
        if not name:
            raise ValueError("Contact name cannot be empty.")
        return name


def display_contacts(contacts):
    """Print contacts in a readable format."""
    if not contacts:
        print("No contacts found.")
        return

    for name, details in contacts.items():
        email = details["email"] or "No email"
        print(f"{name}: {details['phone']} | {email}")


def run():
    """Run the interactive contact-book menu."""
    contact_book = ContactBook()
    menu = (
        "\n1. Add contact\n"
        "2. Search contacts\n"
        "3. Update contact\n"
        "4. Delete contact\n"
        "5. Show all contacts\n"
        "6. Exit"
    )

    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Name: ")
                phone = input("Phone: ")
                email = input("Email (optional): ")
                contact_book.add_contact(name, phone, email)
                print("Contact added.")
            elif choice == "2":
                display_contacts(contact_book.search_contacts(input("Search: ")))
            elif choice == "3":
                name = input("Name: ")
                phone = input("New phone (press Enter to keep current): ")
                email = input("New email (press Enter to keep current): ")
                contact_book.update_contact(name, phone or None, email or None)
                print("Contact updated.")
            elif choice == "4":
                contact_book.delete_contact(input("Name: "))
                print("Contact deleted.")
            elif choice == "5":
                display_contacts(contact_book.contacts)
            elif choice == "6":
                print("Goodbye!")
                return
            else:
                print("Please choose a number from 1 to 6.")
        except (KeyError, ValueError) as error:
            print(error)


if __name__ == "__main__":
    run()