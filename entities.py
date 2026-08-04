from dataclasses import dataclass
from sqlite3 import Row


@dataclass(slots=True)
class Contact:
    id: int | None = None
    first_name: str = ""
    last_name: str = ""
    mobile: str = ""
    landline: str = ""
    address: str = ""
    notes: str = ""

    @property
    def full_name(self) -> str:
        return " ".join(
            part for part in (self.first_name, self.last_name) if part
        ).strip()

    @property
    def has_phone(self) -> bool:
        return bool(self.mobile or self.landline)

    @classmethod
    def from_row(cls, record: Row):
        return cls(
            id=record["id"],
            first_name=record["first_name"] or "",
            last_name=record["last_name"] or "",
            mobile=record["mobile"] or "",
            landline=record["landline"] or "",
            address=record["address"] or "",
            notes=record["notes"] or "",
        )

    def as_tuple(self):
        return (
            self.first_name,
            self.last_name,
            self.mobile,
            self.landline,
            self.address,
            self.notes,
        )

    def as_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mobile": self.mobile,
            "landline": self.landline,
            "address": self.address,
            "notes": self.notes,
        }

    def update(self, **fields):
        for key, value in fields.items():
            if hasattr(self, key):
                setattr(self, key, value)