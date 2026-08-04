from entities import Contact
from repository import ContactRepository


class ContactService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def list_contacts(self):
        rows = self.repository.fetch_all()
        return [Contact.from_row(row) for row in rows]

    def search_contacts(self, keyword: str):
        keyword = keyword.strip()

        if not keyword:
            return self.list_contacts()

        rows = self.repository.search(keyword)
        return [Contact.from_row(row) for row in rows]

    def get_contact(self, contact_id: int):
        row = self.repository.fetch(contact_id)

        if row is None:
            return None

        return Contact.from_row(row)

    def save_contact(self, contact: Contact):
        self._validate(contact)

        if contact.id is None:
            contact.id = self.repository.create(*contact.as_tuple())
            return contact

        self.repository.update(
            contact.id,
            *contact.as_tuple(),
        )

        return contact

    def delete_contact(self, contact_id: int):
        self.repository.remove(contact_id)

    def delete_everything(self):
        self.repository.remove_all()

    def contact_count(self):
        return self.repository.total()

    def _validate(self, contact: Contact):
        fields = (
            contact.first_name,
            contact.last_name,
            contact.mobile,
            contact.landline,
        )

        if not any(value.strip() for value in fields):
            raise ValueError(
                "At least one of the following fields is required: "
                "first name, last name, mobile or landline."
            )

    def shutdown(self):
        self.repository.close()