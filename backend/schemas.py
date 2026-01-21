from pydantic import BaseModel
from typing import Optional

class RecommendRequest(BaseModel):
    user_id: Optional[int] = None
    item_name: Optional[str] = None
    method: str