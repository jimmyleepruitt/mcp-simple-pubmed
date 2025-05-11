
import asyncio
import json
import sys

async def search_pubmed(query: str, max_results: int = 10):
    """Simple function to search PubMed using the MCP server."""
    # Import the MCP client library for local testing
    from mcp.client import Client
    
    # Connect to the MCP server running locally
    client = Client("stdio")
    await client.connect()
    
    # Initialize the client
    await client.initialize("test-client")
    
    # List available tools to verify the server is working
    tools = await client.list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Call the search_pubmed tool
    result = await client.call_tool("search_pubmed", {
        "query": query,
        "max_results": max_results
    })
    
    # Print the formatted results
    if result and result[0].text:
        try:
            data = json.loads(result[0].text)
            print(f"\nFound {len(data)} results for '{query}':\n")
            for i, article in enumerate(data, 1):
                print(f"{i}. {article.get('title', 'No title')}")
                print(f"   Authors: {', '.join(article.get('authors', ['Unknown']))}")
                print(f"   Journal: {article.get('journal', 'Unknown')}")
                print(f"   PMID: {article.get('pmid', 'Unknown')}")
                print(f"   DOI: {article.get('doi', 'Not available')}")
                print(f"   Abstract: {article.get('abstract', 'No abstract')[:150]}...")
                print()
        except json.JSONDecodeError:
            print("Could not parse results:", result[0].text)
    else:
        print("No results or error occurred")
    
    # Disconnect from the server
    await client.shutdown()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use the command line argument as the search query
        query = sys.argv[1]
        max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        asyncio.run(search_pubmed(query, max_results))
    else:
        print("Please provide a search query as a command-line argument.")
        print("Example: python test_pubmed.py 'covid vaccine' 5")
