# my_server.py
from fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP("Demo Analysis Tools")

@mcp.tool()
def calculate_compound_interest(principal: float, rate: float, years: int) -> str:
    """Calculates compound interest over a period of years."""
    amount = principal * ((1 + (rate / 100)) ** years)
    interest = amount - principal
    return f"Total Value: ${amount:,.2f} | Interest Earned: ${interest:,.2f}"

@mcp.tool()
def get_system_status() -> str:
    """Returns basic system health status."""
    return "All local systems operational. Memory usage: 42%, Storage free: 120GB."

if __name__ == "__main__":
    mcp.run(transport="stdio")