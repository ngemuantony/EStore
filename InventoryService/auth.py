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

async def verify_admin(token: str) -> bool:
    user = await verify_user_token(token)
    if not user:
        return False
    # You can add more sophisticated admin checks here
    # For now, we'll consider verified users as admins
    return user["is_verified"]

def check_product_owner(product, user_id: int):
    if product.created_by != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to modify this product"
        )
