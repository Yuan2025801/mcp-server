import logging
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from .resource.vpn_resource import VPNSDK

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("VPN MCP Server", port=int(os.getenv("PORT", "8000")))

vpn_resource = VPNSDK(
    region=os.getenv("VOLCENGINE_REGION"),
    ak=os.getenv("VOLCENGINE_ACCESS_KEY"),
    sk=os.getenv("VOLCENGINE_SECRET_KEY"),
    host=os.getenv("VOLCENGINE_ENDPOINT"),
)


@mcp.tool(name="describe_vpn_connection", description="查询指定的IPsec连接详情")
def describe_vpn_connection(vpn_connection_id: str) -> dict[str, Any]:
    """查询指定的 IPsec 连接详情。

    Args:
        vpn_connection_id: IPsec 连接的ID。
    """
    req = {"VpnConnectionId": vpn_connection_id}
    resp = vpn_resource.describe_vpn_connection_attributes(req)
    return resp.to_dict()
