from neo4j import GraphDatabase
from tqdm import tqdm

class Database:
    def __init__(self, uri, auth) -> None:
        self.uri = uri
        self.auth = auth
        self.driver = None

    def connect(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=self.auth)
            with self.driver.session() as session:
                session.run("RETURN 1")
                print("Connected to database.")
        except Exception as e:
            print(f"Failed to connect. Error: {e}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()
            print("Connection closed")


class DataManager:
    def __init__(self, driver, batch_size=1000) -> None:  
        self.driver = driver
        self.batch_size = batch_size

    def create_node(self, nodes):
        try:
            with self.driver.session() as session:
                with session.begin_transaction() as tx:
                    for label, properties in nodes:
                        query = f"CREATE (n:{label} {{"
                        query += ", ".join([f"{k}: ${k}" for k in properties.keys()])
                        query += "})"
                        tx.run(query, properties)
                    tx.commit()
        except Exception as e:
            return f"error {e}"

    def load_data(self, data):
        total_nodes = len(data)
        for i in tqdm(range(0, total_nodes, self.batch_size), desc="Creating nodes", ncols=100):
            batch = data[i:i + self.batch_size]
            nodes = [(item['label'], item['properties']) for item in batch]
            self.create_node(nodes)

    def address_info(self, address):
        query = """
            MATCH p=(a:addresses {address: $address})-[r]->(t:inputs {recipient: $address})
            RETURN t, r, a
            UNION
            MATCH p=(a:addresses {address: $address})-[r]->(t:outputs {recipient: $address})
            RETURN t, r, a
        """

        with self.driver.session() as session:
            result = session.run(query, address=address)
            nodes = []
            for record in result:
                node_data = {
                    'transaction': dict(record['t'].items()),
                    'relationship': {'type': record['r'].type},
                }
                nodes.append(node_data)

        return nodes

    def relationships(self):
        queries = [
            """
            MATCH (a:addresses)
            WITH a
            LIMIT {batch_size}
            OPTIONAL MATCH (o:outputs) 
            WHERE a.address = o.recipient 
            WITH a, o
            WHERE o IS NOT NULL
            MERGE (a)-[:OUTPUT_TRANSACTION]->(o);
            """,
            """
            MATCH (a:addresses)
            WITH a
            LIMIT {batch_size}
            OPTIONAL MATCH (i:inputs) 
            WHERE a.address = i.recipient 
            WITH a, i
            WHERE i IS NOT NULL
            MERGE (a)-[:INPUT_TRANSACTION]->(i);
            """
        ]
        with self.driver.session() as session:
            for query in queries:
                total_addresses = session.run("MATCH (a:addresses) RETURN count(a) AS count").single()["count"]
                for _ in tqdm(range(0, total_addresses, self.batch_size), desc="Creating relationships", ncols=100):
                    session.run(query.format(batch_size=self.batch_size))


    
    def db_show(self):
        query = "CALL db.info() YIELD name RETURN name"
        message = []
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                message.append(record)
                
        return message

    def create_indexes(self):
        queries = [
            "CREATE INDEX address_index IF NOT EXISTS FOR (a:addresses) ON (a.address)",
            "CREATE INDEX output_recipient_index IF NOT EXISTS FOR (o:outputs) ON (o.recipient)",
            "CREATE INDEX input_recipient_index IF NOT EXISTS FOR (i:inputs) ON (i.recipient)"
        ]
        with self.driver.session() as session:
            for query in queries:
                session.run(query)

        print("New indexes have been created.")
    
    def drop_indexes(self):
        drop_index_queries = [
            "DROP INDEX index_name IF EXISTS"
            for index_name in self.get_existing_indexes()
        ]
        with self.driver.session() as session:
            for query in drop_index_queries:
                session.run(query)
        print("All indexes have been dropped.")

    def get_existing_indexes(self):
        existing_indexes = []
        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")
            for record in result:
                index_name = record["name"]
                existing_indexes.append(index_name)
        return existing_indexes