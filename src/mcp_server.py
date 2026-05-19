from mcp.server.fastapi import Context, Server
from src.services.memory import MemoryService
from src.services.search import SearchService
import uvicorn
import os

app = Server("Universal AI Layer")
memory_service = MemoryService()
search_service = SearchService()

@app.tool()
async def recall_memory(query: str, project_id: str = None) -> str:
    """Search for relevant memories in the Universal AI Layer."""
    results = await search_service.hybrid_search(query, project_id)
    return str(results)

@app.tool()
async def store_memory(text: str, project_id: str = None) -> str:
    """Store a new memory in the Universal AI Layer."""
    await memory_service.add_memory(raw_text=text, project_id=project_id)
    return "Memory stored successfully."

if __name__ == "__main__":
    # MCP servers can run over stdio or SSE. This setup uses SSE via FastAPI.
    from mcp.server.fastapi import McpFastAPI
    mcp_app = McpFastAPI(app)
    uvicorn.run(mcp_app, host="0.0.0.0", port=8001)
