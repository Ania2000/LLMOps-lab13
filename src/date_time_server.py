import datetime

from fastmcp import FastMCP

mcp = FastMCP("Date and time server")


@mcp.tool(description="Get current date in format YYYY-MM-DD")
def get_current_date() -> str:
    return datetime.date.today().isoformat()


@mcp.tool(description="Get current date and time in ISO 8601 format up to seconds")
def get_current_datetime() -> str:
    now = datetime.datetime.now().replace(microsecond=0)
    return now.isoformat()


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8002
    )
