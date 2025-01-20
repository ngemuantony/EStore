import requests
from fastapi import HTTPException
from typing import Dict

INVENTORY_SERVICE_URL = "http://localhost:8000"

class InventoryService:
    @staticmethod
    async def get_product(product_id: str) -> Dict:
        response = requests.get(f'{INVENTORY_SERVICE_URL}/products/{product_id}')
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
        return response.json()

    @staticmethod
    async def update_quantity(product_id: str, new_quantity: int) -> Dict:
        update_response = requests.patch(
            f'{INVENTORY_SERVICE_URL}/products/{product_id}/quantity', 
            json={"quantity": new_quantity}
        )
        
        if update_response.status_code != 200:
            raise HTTPException(
                status_code=500, 
                detail="Failed to update inventory quantity"
            )
        return update_response.json()
