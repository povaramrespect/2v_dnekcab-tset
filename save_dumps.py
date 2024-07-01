from config import address, keys
from services import get_dump
from database import DataManager, Database

db = Database(address, keys)

def store_dumps(urls):
    try:
        db.connect()
        driver = DataManager(db.driver)
        
        for url in urls:
            data = get_dump(f'{url}')
            driver.load_data(data)

        print("Data successfully loaded and saved to database.")

        try:
            driver.create_indexes()

        except Exception:
            driver.drop_indexes()
            driver.create_indexes()

        driver.relationships()

        db.close()

    except Exception as e:
        print(f"Error: {e}")


urls = ["https://gz.blockchair.com/zcash/inputs/blockchair_zcash_inputs_20240627.tsv.gz",
        "https://gz.blockchair.com/zcash/outputs/blockchair_zcash_outputs_20240627.tsv.gz",
        "https://gz.blockchair.com/zcash/addresses/blockchair_zcash_addresses_latest.tsv.gz"]

store_dumps(urls)
