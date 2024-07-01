# Backend. Тестовое задание v2

**Bitcoin from Blockchair**

**Требования**

    > Python версии X.X или выше
    > Установленные библиотеки, указанные в requirements.txt (pip install -r requirements.txt)
    > Для подключения к базе данных необходимо указать адрес и данные авторизации в файле config.py:

**Запуск приложения FastAPI**

Для запуска приложения FastAPI используйте команду:

uvicorn src.main:app --reload

**FastAPI app**

> Эндпоинт /relationships автоматически создает отношения между транзакциями и адресами, у которых совпадает адрес кошелька.
> Эндпоинт /address_info/{address} выводит информацию о транзакциях, в которых присутствует указанный адрес кошелька.

**Пример использования**

1. Запуск проекта neo4j, ввод данных для подключения в config.py

2. save_dumps.py - Загрузка архивов в базу neo4j

-> urls = ["https://gz.blockchair.com/zcash/inputs/blockchair_zcash_inputs_20240627.tsv.gz",
        "https://gz.blockchair.com/zcash/outputs/blockchair_zcash_outputs_20240627.tsv.gz",
        "https://gz.blockchair.com/zcash/addresses/blockchair_zcash_addresses_latest.tsv.gz"]

3. **Не работает** Запуск /relationships для создания связей между узлами

4. **Не работает** /address_info/{address} Поиск транзакций по кошельку

