from fastapi import APIRouter
from database import Database, DataManager
from config import address, keys

router = APIRouter()

db = Database(address, keys)

@router.post("/address_transactions/{address}")
async def show_address_transactions(address):
    try:
        db.connect()
        driver = DataManager(db.driver)
        result = driver.address_info(address)
        db.close()

    except Exception as e:
        return {"error": str(e)} 
    
    if result:
        return result
    else:
        return {"message": f"Transactions with address {address} not found."}
        
