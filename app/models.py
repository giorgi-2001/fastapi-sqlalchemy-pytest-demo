from sqlalchemy import CheckConstraint
from .database import Base, int_pk, str_nullable, str_uniq, Mapped


class Product(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str_nullable]

    def __repr__(self):
        return self.name
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    __table_args__ = (CheckConstraint("LENGTH(name) > 1", name="name_min_length"),)