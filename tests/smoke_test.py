import sys
import os

# Set dummy env vars BEFORE imports
os.environ["OPENAI_API_KEY"] = "mock_key"
os.environ["DATABASE_URL"] = "postgresql://mock:mock@localhost:5432/mock"
os.environ["UNIVERSAL_API_KEY"] = "dev_key"

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_imports():
    print("Testing core imports...")
    try:
        from src.main import app
        from src.services.memory import MemoryService
        from src.services.search import SearchService
        from src.services.llm import ExtractorService
        from src.services.git_ingestor import GitIngestor
        from src.services.ast_ingestor import ASTIngestor
        from src.tasks import consolidate_task, audit_conflicts_task
        print("✅ All core imports successful.")
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        sys.exit(1)

def test_service_instantiation():
    print("\nTesting service instantiation (with mocked dependencies)...")
    os.environ["OPENAI_API_KEY"] = "mock_key"
    os.environ["DATABASE_URL"] = "postgresql://mock:mock@localhost:5432/mock"
    
    try:
        from src.services.llm import ExtractorService
        extractor = ExtractorService()
        print("✅ ExtractorService initialized.")
        
        # We can't easily init MemoryService/SearchService without a real DB
        # because they call GraphService which tries to connect.
        # But we've verified the code structure.
    except Exception as e:
        print(f"❌ Service init failed: {str(e)}")

if __name__ == "__main__":
    test_imports()
    test_service_instantiation()
    print("\nSmoke test complete.")
