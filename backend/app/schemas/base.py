from pydantic import BaseModel

class BaseSchema(BaseModel):
    """Base class for Pydantic schemas with common configuration."""
    model_config = {
        "from_attributes": True,
    }
