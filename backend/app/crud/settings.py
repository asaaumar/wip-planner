from sqlalchemy.orm import Session

from app.models.settings import Settings
from app.schemas.settings import SettingsUpdate


def get_settings(db: Session) -> Settings:
    """Get the settings (always returns the single row with id=1)"""
    settings = db.query(Settings).filter(Settings.id == 1).first()
    if not settings:
        # Create default settings if they don't exist
        settings = Settings(id=1, wip_limit=1)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def update_settings(db: Session, settings_update: SettingsUpdate) -> Settings:
    """Update the settings"""
    settings = get_settings(db)
    settings.wip_limit = settings_update.wip_limit
    db.commit()
    db.refresh(settings)
    return settings
