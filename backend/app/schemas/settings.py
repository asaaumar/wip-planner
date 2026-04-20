from pydantic import BaseModel, Field


class SettingsResponse(BaseModel):
    """Schema for settings response"""
    wip_limit: int = Field(..., ge=1, description="Work-in-progress limit (minimum 1)")

    class Config:
        from_attributes = True


class SettingsUpdate(BaseModel):
    """Schema for updating settings"""
    wip_limit: int = Field(..., ge=1, description="Work-in-progress limit (minimum 1)")
