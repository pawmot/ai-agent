from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")


@mcp.tool
def power(a: int, b: int) -> int:
    """Raise a to the power of b"""
    return a ** b


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8123)
