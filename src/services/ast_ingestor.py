import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import os
from src.services.graph import GraphService
from typing import List

class ASTIngestor:
    def __init__(self):
        self.PY_LANGUAGE = Language(tspython.language())
        self.parser = Parser(self.PY_LANGUAGE)
        self.graph = GraphService()

    def ingest_directory(self, path: str, project_id: str):
        """Walks through a directory and parses all Python files."""
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self.parse_file(file_path, project_id)

    def parse_file(self, file_path: str, project_id: str):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        tree = self.parser.parse(bytes(content, "utf8"))
        root_node = tree.root_node
        file_name = os.path.basename(file_path)
        
        # v4.0: Capture File node
        self.graph.add_entity(file_name, "FILE", project_id)

        # Advanced extraction using Tree-Sitter Queries
        self._extract_with_queries(root_node, content, file_name, project_id)

    def _extract_with_queries(self, root_node, content, file_name, project_id):
        # Query for function and class definitions with more context
        query_text = """
        (class_definition
            name: (identifier) @class.name) @class.def
            
        (function_definition
            name: (identifier) @func.name
            parameters: (parameters) @func.params
            return_type: (type)? @func.return) @func.def
            
        (call
            function: (identifier) @call.name) @call.stmt
        """
        query = self.PY_LANGUAGE.query(query_text)
        captures = query.captures(root_node)

        current_class = None
        current_func = None

        for node, tag in captures:
            node_text = content[node.start_byte:node.end_byte]

            if tag == "class.name":
                current_class = node_text
                self.graph.add_entity(current_class, "CLASS", project_id)
                self.graph.add_relation(file_name, current_class, "CONTAINS", project_id)
            
            elif tag == "func.name":
                current_func = node_text
                full_name = f"{current_class}.{current_func}" if current_class else current_func
                self.graph.add_entity(full_name, "FUNCTION", project_id)
                
                parent_entity = current_class if current_class else file_name
                self.graph.add_relation(parent_entity, full_name, "CONTAINS", project_id)

            elif tag == "call.name":
                # Build the Call Graph (Dependencies)
                target_func = node_text
                source_entity = f"{current_class}.{current_func}" if current_class and current_func else (current_func or file_name)
                
                if target_func != current_func: # Avoid self-recursion noise for now
                    self.graph.add_relation(source_entity, target_func, "CALLS", project_id)

    def _get_node_text(self, node) -> str:
        if not node: return "unknown"
        return node.text.decode("utf8")
