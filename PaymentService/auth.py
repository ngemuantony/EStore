from fastapi import HTTPException
import requests
from typing import Optional

USER_SERVICE_URL = "http://localhost:8002"

async def verify_user_token(token: str) -> Optional[dict]:
    try:
        response = requests.get(
            f"{USER_SERVICE_URL}/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def check_order_owner(order: dict, user_id: int):
    if order["user_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this order"
        )
