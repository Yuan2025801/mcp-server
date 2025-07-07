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

from pydantic import BaseModel, Field, constr
from mcp.types import CallToolResult, TextContent

from .clients import VPNClient
from functools import lru_cache

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


_CLIENT_CACHE: dict[tuple[str | None, str | None], VPNClient] = {}


def _get_vpn_client(region: str | None = None) -> VPNClient:
    """Create or reuse a VPN client instance using STS credentials."""
    creds = {}
    try:
        creds = _read_sts()
    except Exception:
        # Fallback to environment variables when STS header missing
        pass

    ak = creds.get("AccessKeyId") or os.getenv("VOLCENGINE_ACCESS_KEY")
    sk = creds.get("SecretAccessKey") or os.getenv("VOLCENGINE_SECRET_KEY")
    session_token = creds.get("SessionToken") or os.getenv("VOLCENGINE_SESSION_TOKEN")
    region = region or os.getenv("VOLCENGINE_REGION")
    host = os.getenv("VOLCENGINE_ENDPOINT")
    key = (ak, region)

    client = _CLIENT_CACHE.get(key)
    if client is None:
        client = VPNClient(
            region=region,
            ak=ak,
            sk=sk,
            host=host,
            session_token=session_token,
            timeout=5,
            max_retries=3,
        )
        _CLIENT_CACHE[key] = client
    return client


class DescribeVpnConnectionSchema(BaseModel):
    """Schema for describe_vpn_connection."""

    vpn_connection_id: constr(strip_whitespace=True, min_length=1) = Field(
        description="IPsec 连接的ID"
    )
    region: str | None = Field(default=None, description="资源所在 Region")


class DescribeVpnGatewaySchema(BaseModel):
    """Schema for describe_vpn_gateway."""

    vpn_gateway_id: constr(strip_whitespace=True, min_length=1) = Field(
        description="VPN 网关ID"
    )
    region: str | None = Field(default=None, description="资源所在 Region")


class DescribeVpnConnectionsSchema(BaseModel):
    """Schema for describe_vpn_connections."""

    page_number: int | None = Field(default=None, description="页码，从1开始")
    page_size: int | None = Field(default=None, description="分页大小")
    vpn_gateway_id: str | None = Field(default=None, description="VPN 网关ID")
    vpn_connection_name: str | None = Field(default=None, description="IPsec连接名称")
    status: str | None = Field(default=None, description="连接状态")
    region: str | None = Field(default=None, description="资源所在 Region")


@mcp.tool(
    name="describe_vpn_connection",
    title="Query VPN Connection / 查询 VPN 连接详情",
    description=(
        '查询指定的IPsec连接详情。\n\n示例：{"vpn_connection_id":"vpn-xxx","region":"cn-beijing"}'
    ),
    inputSchema=DescribeVpnConnectionSchema.schema(),
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def describe_vpn_connection(
    vpn_connection_id: str,
    region: str | None = None,
) -> DescribeVpnConnectionAttributesResponse | CallToolResult:
    """查询指定的 IPsec 连接详情。

    Args:
        vpn_connection_id: IPsec 连接的ID。
    """
    vpn_client = _get_vpn_client(region=region)
    req = DescribeVpnConnectionAttributesRequest(vpn_connection_id=vpn_connection_id)
    try:
        resp = vpn_client.describe_vpn_connection_attributes(req)
        return resp
    except Exception as exc:
        logger.exception("Error calling describe_vpn_connection")
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"查询失败：{exc}")],
        )


@mcp.tool(
    name="describe_vpn_gateway",
    title="Query VPN Gateway / 查询 VPN 网关详情",
    description=(
        '查询指定的VPN网关详情。\n\n示例：{"vpn_gateway_id":"vgw-xxx","region":"cn-beijing"}'
    ),
    inputSchema=DescribeVpnGatewaySchema.schema(),
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def describe_vpn_gateway(
    vpn_gateway_id: str,
    region: str | None = None,
) -> DescribeVpnGatewayAttributesResponse | CallToolResult:
    """查询指定 VPN 网关的详情。"""
    vpn_client = _get_vpn_client(region=region)
    req = DescribeVpnGatewayAttributesRequest(vpn_gateway_id=vpn_gateway_id)
    try:
        resp = vpn_client.describe_vpn_gateway_attributes(req)
        return resp
    except Exception as exc:
        logger.exception("Error calling describe_vpn_gateway")
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"查询失败：{exc}")],
        )


@mcp.tool(
    name="describe_vpn_connections",
    title="Query VPN Connections / 查询 VPN 连接列表",
    description=(
        '查询满足条件的IPsec连接。\n\n示例：{"vpn_gateway_id":"vgw-xxx","page_size":10}'
    ),
    inputSchema=DescribeVpnConnectionsSchema.schema(),
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def describe_vpn_connections(
    page_number: int | None = None,
    page_size: int | None = None,
    vpn_gateway_id: str | None = None,
    vpn_connection_name: str | None = None,
    status: str | None = None,
    region: str | None = None,
) -> DescribeVpnConnectionsResponse | CallToolResult:
    """查询IPsec连接列表。"""
    vpn_client = _get_vpn_client(region=region)
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
    except Exception as exc:
        logger.exception("Error calling describe_vpn_connections")
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"查询失败：{exc}")],
        )
