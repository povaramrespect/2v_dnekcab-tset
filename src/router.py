from fastapi import APIRouter
from database import Database, DataManager
from config import address, keys

router = APIRouter()

db = Database(address, keys)

@router.post("/address_info/{address}")
async def show_address_info(address):
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

@router.post("/relationships")
async def find_relationships():
    try:
        db.connect()
        driver = DataManager(db.driver)
        driver.relationships()
        db.close()

    except Exception as e:
        return {"error": str(e)} 
    
    return {"message": f"Nodes relationships updated"}
        
    
@router.get("/db")
async def show_db():
    db.connect()
    driver = DataManager(db.driver)
    message = driver.db_show()
    db.close()

    return message