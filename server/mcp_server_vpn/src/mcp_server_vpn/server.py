import logging
import os

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("VPN MCP Server", port=int(os.getenv("PORT", "8000")))

# TODO: Add VPN related tools here
