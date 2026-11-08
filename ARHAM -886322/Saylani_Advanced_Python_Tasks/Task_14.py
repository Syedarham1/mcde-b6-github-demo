import json
import os

class ContactManager:
    def __init__(self, storage_path="contacts.json"):
        self.storage_path = storage_path
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if not os.path.exists(self.storage_path):
            return []
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
  
            backup_path = self.storage_path + ".bak"
            if os.path.exists(self.storage_path):
                os.rename(self.storage_path, backup_path)
            return []

    def save_contacts(self):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, indent=4)

    def add_contact(self, contact_id, name, phone, email):
        if any(c['id'] == contact_id for c in self.contacts):
            raise ValueError("Contact ID already exists.")
        self.contacts.append({'id': contact_id, 'name': name, 'phone': phone, 'email': email})
        self.save_contacts()

    def search(self, query):
        q = query.lower()
        return [c for c in self.contacts if q in c['name'].lower() or q in c['phone'] or q in c['email'].lower()]