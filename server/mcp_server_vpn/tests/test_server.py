import os
import sys
import types
import pytest
import asyncio

# Provide dummy SDK modules so that server module can be imported
core = types.ModuleType('volcenginesdkcore')
core.Configuration = type('Configuration', (), {})
core.ApiClient = object
vpn_mod = types.ModuleType('volcenginesdkvpn')
vpn_api_mod = types.ModuleType('volcenginesdkvpn.api.vpn_api')


class DummyApi: pass


vpn_api_mod.VPNApi = DummyApi
models_mod = types.ModuleType('volcenginesdkvpn.models')


class Resp: pass


class BaseReq:
    def __init__(self, **kwargs):
        pass


models_mod.DescribeVpnConnectionAttributesRequest = BaseReq
models_mod.DescribeVpnConnectionAttributesResponse = Resp
models_mod.DescribeVpnConnectionsRequest = BaseReq
models_mod.DescribeVpnConnectionsResponse = Resp
models_mod.DescribeVpnGatewayAttributesRequest = BaseReq
models_mod.DescribeVpnGatewayAttributesResponse = Resp
sys.modules['volcenginesdkcore'] = core
sys.modules['volcenginesdkvpn'] = vpn_mod
sys.modules['volcenginesdkvpn.api'] = types.ModuleType('api')
sys.modules['volcenginesdkvpn.api.vpn_api'] = vpn_api_mod
sys.modules['volcenginesdkvpn.models'] = models_mod

# Dummy mcp modules
mcp_fastmcp = types.ModuleType('mcp.server.fastmcp')


class FastMCP:
    def __init__(self, *a, **kw):
        pass

    def tool(self, **kw):
        def deco(func):
            return func

        return deco

    def get_context(self):
        class Ctx:
            request_context = types.SimpleNamespace(request=None)

        return Ctx()


Context = type('Context', (), {})
mcp_fastmcp.FastMCP = FastMCP
mcp_fastmcp.Context = Context
sys.modules['mcp'] = types.ModuleType('mcp')
sys.modules['mcp.server'] = types.ModuleType('server')
sys.modules['mcp.server.fastmcp'] = mcp_fastmcp
mcp_session = types.ModuleType('mcp.server.session')


class ServerSession: ...


mcp_session.ServerSession = ServerSession
sys.modules['mcp.server.session'] = mcp_session
types_mod = types.ModuleType('mcp.types')


class CallToolResult:
    def __init__(self, isError=False, content=None):
        self.isError = isError
        self.content = content


class TextContent:
    def __init__(self, **kwargs):
        pass


types_mod.CallToolResult = CallToolResult
types_mod.TextContent = TextContent
sys.modules['mcp.types'] = types_mod

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from mcp_server_vpn import server
from mcp.types import CallToolResult


class StubClient:
    def __init__(self, exc: Exception | None = None):
        self.exc = exc

    def describe_vpn_connection_attributes(self, req):
        if self.exc:
            raise self.exc
        return 'ok'


def test_describe_vpn_connection_success(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient())
    result = asyncio.run(server.describe_vpn_connection('id'))
    assert result == 'ok'


def test_describe_vpn_connection_error(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient(Exception('boom')))
    result = asyncio.run(server.describe_vpn_connection('id'))
    assert isinstance(result, CallToolResult) and result.isError
