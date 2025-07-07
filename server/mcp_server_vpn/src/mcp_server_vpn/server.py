import base64
import json
import logging
import os

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from starlette.requests import Request
from volcenginesdkvpn.models import (
    DescribeVpnConnectionAttributesRequest,
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnConnectionsRequest,
    DescribeVpnConnectionsResponse,
    DescribeVpnGatewayAttributesRequest,
    DescribeVpnGatewayAttributesResponse,
)

from .clients import VPNClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
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
    return VPNClient(
        region=os.getenv("VOLCENGINE_REGION"),
        ak=os.getenv("VOLCENGINE_ACCESS_KEY"),
        sk=os.getenv("VOLCENGINE_SECRET_KEY"),
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
    req = DescribeVpnConnectionAttributesRequest(vpn_connection_id=vpn_connection_id)
    try:
        resp = vpn_client.describe_vpn_connection_attributes(req)
        return resp
    except Exception:
        logger.exception("Error calling describe_vpn_connection")
        raise


@mcp.tool(name="describe_vpn_gateway", description="查询指定的VPN网关详情")
def describe_vpn_gateway(
    vpn_gateway_id: str,
) -> DescribeVpnGatewayAttributesResponse:
    """查询指定 VPN 网关的详情。"""
    vpn_client = _get_vpn_client()
    req = DescribeVpnGatewayAttributesRequest(vpn_gateway_id=vpn_gateway_id)
    try:
        resp = vpn_client.describe_vpn_gateway_attributes(req)
        return resp
    except Exception:
        logger.exception("Error calling describe_vpn_gateway")
        raise


@mcp.tool(name="describe_vpn_connections", description="查询满足条件的IPsec连接")
def describe_vpn_connections(
    page_number: int | None = None,
    page_size: int | None = None,
    vpn_gateway_id: str | None = None,
    vpn_connection_name: str | None = None,
    status: str | None = None,
) -> DescribeVpnConnectionsResponse:
    """查询IPsec连接列表。"""
    vpn_client = _get_vpn_client()
    req = DescribeVpnConnectionsRequest(
        page_number=page_number,
        page_size=page_size,
        vpn_gateway_id=vpn_gateway_id,
        vpn_connection_name=vpn_connection_name,
        status=status,
    )
    try:
        resp = vpn_client.describe_vpn_connections(req)
        return resp
    except Exception:
        logger.exception("Error calling describe_vpn_connections")
        raise
