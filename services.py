from tqdm import tqdm
from urllib import request

import gzip 
import re

def get_dump(url):
    try:
        match = re.search(r'https://gz\.blockchair\.com/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/', url)

        currency = match.group(1).replace('-', '_')
        dump_type = currency + "_" + match.group(2)
        print(f"Start reading: {dump_type}")

        with request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as f:
                lines = f.readlines()

        print("Reading completed.")

        columns = lines[0].decode('utf-8').strip().split('\t')
        data = lines_format(lines, columns, match.group(2), currency)
            
        return data
        
    except Exception as e:
        raise Exception(f"Ошибка при получении данных: {e}")

def lines_format(lines, columns, dump_type, currency):
    q_lines = []

    for line in tqdm(lines[1:], total=len(lines), desc="Formatting lines", ncols=100):
        values = line.decode('utf-8').strip().split('\t')
        properties = dict(zip(columns, values))
        properties['currency'] = currency
        q_lines.append({"label": dump_type, "properties": properties})  

    return q_lines
      
