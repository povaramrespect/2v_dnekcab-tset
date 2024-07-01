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
    def __init__(self, driver) -> None:  
        self.driver = driver

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
        batch_size = 1000
        for i in tqdm(range(0, total_nodes, batch_size), desc="Creating nodes", ncols=100):
            batch = data[i:i + batch_size]
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

        print(nodes)

        return nodes

    def relationships(self):
        query = """
            MATCH (a:addresses)
            OPTIONAL MATCH (i:inputs)
            WHERE a.address = i.recipient
            MERGE (a)-[:RECEIVED]->(i)
            WITH a, i
            OPTIONAL MATCH (o:outputs)
            WHERE a.address = o.recipient
            MERGE (a)-[:SENT]->(o)
            WITH a, i, o
            RETURN a, i, o
        """

        with self.driver.session() as session:
            session.run(query)


    
    def db_show(self):
        query = "CALL db.info() YIELD name RETURN name"
        message = []
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                message.append(record)
                
        return message
