from datetime import datetime
from uuid import uuid4


class Session:
    def __init__(self, user_id: int):
        self.id = str(uuid4())
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.is_active = True
        self.refresh_token = None
