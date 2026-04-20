from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.settings import SettingsResponse, SettingsUpdate
from app.crud import settings as settings_crud

router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)


@router.get("/", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db)):
    """
    Get current settings
    
    Returns the current WIP limit configuration.
    """
    settings = settings_crud.get_settings(db)
    return settings


@router.put("/", response_model=SettingsResponse)
def update_settings(settings_update: SettingsUpdate, db: Session = Depends(get_db)):
    """
    Update settings
    
    Updates the WIP limit configuration.
    
    - **wip_limit**: Required, minimum value is 1
    """
    settings = settings_crud.update_settings(db, settings_update)
    return settings
