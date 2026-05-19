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
        
        # Simple extraction: Find classes and their methods
        # In a real app, this would be much more sophisticated (identifying imports, etc.)
        self._extract_definitions(root_node, os.path.basename(file_path), project_id)

    def _extract_definitions(self, node, file_name, project_id):
        # We'll use a simple recursive walk for this demonstration
        for child in node.children:
            if child.type == "class_definition":
                class_name = self._get_node_text(child.child_by_field_name("name"))
                self.graph.add_entity(class_name, "CLASS", project_id)
                self.graph.add_relation(file_name, class_name, "CONTAINS", project_id)
            
            elif child.type == "function_definition":
                func_name = self._get_node_text(child.child_by_field_name("name"))
                self.graph.add_entity(func_name, "FUNCTION", project_id)
                self.graph.add_relation(file_name, func_name, "CONTAINS", project_id)
            
            self._extract_definitions(child, file_name, project_id)

    def _get_node_text(self, node) -> str:
        if not node: return "unknown"
        return node.text.decode("utf8")
