from sqlalchemy import Column, Integer

from app.db.session import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, default=1)
    wip_limit = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<Settings(id={self.id}, wip_limit={self.wip_limit})>"
