# Backend. Тестовое задание v2

**Bitcoin from Blockchair**

**Требования**

    > Python версии 11 или выше
    > Установленные библиотеки, указанные в requirements.txt (pip install -r requirements.txt)
    > Для подключения к базе данных необходимо указать адрес и данные авторизации в файле config.py:

**Запуск**

Для запуска приложения FastAPI ввод команды в консоль:

uvicorn src.main:app --reload

Для записи архивов 

python save_dumps.py

**FastAPI app**

> Эндпоинт /address_info/{address} выводит информацию о транзакциях, в которых присутствует указанный адрес кошелька.
> /db - Просмотр имени подключенной базы данных

**Пример использования**

1. Запуск проекта neo4j, ввод данных для подключения в config.py

2. save_dumps.py - Загрузка архивов в базу neo4j

-> Указание urls для загрузки в базу (список ссылок на архивы) = ["https://gz.blockchair.com/zcash/inputs/blockchair_zcash_inputs_20240627.tsv.gz",
        "https://gz.blockchair.com/zcash/outputs/blockchair_zcash_outputs_20240627.tsv.gz",
        "https://gz.blockchair.com/zcash/addresses/blockchair_zcash_addresses_latest.tsv.gz"]

3. Запуск приложения FastAPI, переход по адресу http://127.0.0.1:8000/docs и взаимодействие с эндпоинтом - /address_transactions/{address}"
для просмотра всех транзакций по кошельку


**Примечание**

> В прогресс баре Creating nodes:  82%|█████████       | 639/780 
> За 1 итерацию создается value - batch_size узлов

> -В файле database.py на 27 строке в классе DataManager задается значение переменной batch_size = 1000. 
> Для ускорения создания узлов и отношений в базе есть возможность пробовать повышать значение(в зависимости от ресурсов компьютера) для ускорения работы.