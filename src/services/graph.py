import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import List, Dict, Any

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/universal_ai_layer")

class GraphService:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(DATABASE_URL)
            self.conn.autocommit = True
            self._initialize_age()
        except Exception as e:
            print(f"⚠️ Warning: Could not connect to Graph Database (Apache Age): {str(e)}")
            self.conn = None

    def _initialize_age(self):
        with self.conn.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS age CASCADE;")
            cursor.execute("LOAD 'age';")
            cursor.execute("SET search_path = ag_catalog, \"$user\", public;")
            # Initialize graph if it doesn't exist
            cursor.execute("""
                SELECT count(*) FROM ag_catalog.ag_graph WHERE name = 'universal_graph';
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("SELECT create_graph('universal_graph');")

    def query(self, cypher_query: str, params: Dict[str, Any] = None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # AGE requires wrapping cypher in a select function
            wrapped_query = f"SELECT * FROM cypher('universal_graph', $$ {cypher_query} $$) as (v agtype);"
            cursor.execute(wrapped_query, params)
            return cursor.fetchall()

    def add_entity(self, name: str, entity_type: str, project_id: str):
        cypher = f"""
            MERGE (e:Entity {{name: '{name}', type: '{entity_type}', project_id: '{project_id}'}})
            RETURN e
        """
        return self.query(cypher)

    def add_relation(self, source_name: str, target_name: str, rel_type: str, project_id: str):
        cypher = f"""
            MATCH (a:Entity {{name: '{source_name}', project_id: '{project_id}'}})
            MATCH (b:Entity {{name: '{target_name}', project_id: '{project_id}'}})
            MERGE (a)-[r:{rel_type} {{project_id: '{project_id}'}}]->(b)
            RETURN r
        """
        return self.query(cypher)

    def get_related_entities(self, entity_name: str, project_id: str):
        cypher = f"""
            MATCH (a:Entity {{name: '{entity_name}', project_id: '{project_id}'}})-[r]->(related)
            RETURN related
        """
        return self.query(cypher)
