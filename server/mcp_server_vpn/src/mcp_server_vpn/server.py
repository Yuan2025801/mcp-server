import base64
import json
import logging
import os

from volcenginesdkvpn.models import (
    DescribeVpnConnectionAttributesRequest,
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnGatewayAttributesRequest,
    DescribeVpnGatewayAttributesResponse,
)

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession
from starlette.requests import Request

from .clients import VPNClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("VPN MCP Server", port=int(os.getenv("PORT", "8000")))


def _read_sts() -> dict:
    """Read STS credentials from the request header or environment."""
    ctx: Context[ServerSession, object] = mcp.get_context()
    req: Request | None = ctx.request_context.request
    auth = (req.headers.get("authorization") if req else None) or os.getenv(
        "authorization"
    )
    if not auth:
        raise ValueError("Missing authorization")
    _, b64 = auth.split(" ", 1) if " " in auth else ("", auth)
    decoded = base64.b64decode(b64)
    return json.loads(decoded)


def _get_vpn_client() -> VPNClient:
    """Create a VPN client instance using STS credentials."""
    creds = _read_sts()
    return VPNClient(
        region=os.getenv("VOLCENGINE_REGION"),
        ak=creds.get("AccessKeyId"),
        sk=creds.get("SecretAccessKey"),
        host=os.getenv("VOLCENGINE_ENDPOINT"),
    )


@mcp.tool(name="describe_vpn_connection", description="查询指定的IPsec连接详情")
def describe_vpn_connection(
    vpn_connection_id: str,
) -> DescribeVpnConnectionAttributesResponse:
    """查询指定的 IPsec 连接详情。

    Args:
        vpn_connection_id: IPsec 连接的ID。
    """
    vpn_client = _get_vpn_client()
    req = DescribeVpnConnectionAttributesRequest(VpnConnectionId=vpn_connection_id)
    resp = vpn_client.describe_vpn_connection_attributes(req)
    return resp


@mcp.tool(name="describe_vpn_gateway", description="查询指定的VPN网关详情")
def describe_vpn_gateway(
    vpn_gateway_id: str,
) -> DescribeVpnGatewayAttributesResponse:
    """查询指定 VPN 网关的详情。"""
    vpn_client = _get_vpn_client()
    req = DescribeVpnGatewayAttributesRequest(VpnGatewayId=vpn_gateway_id)
    resp = vpn_client.describe_vpn_gateway_attributes(req)
    return resp
