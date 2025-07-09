import os
import sys
import types
import pytest
import asyncio

# Provide dummy SDK modules so that server module can be imported
core = types.ModuleType('volcenginesdkcore')
core.Configuration = type('Configuration', (), {})
core.ApiClient = object
core.rest = types.ModuleType('rest')
core.rest.ApiException = type('ApiException', (Exception,), {})
vpn_mod = types.ModuleType('volcenginesdkvpn')
vpn_api_mod = types.ModuleType('volcenginesdkvpn.api.vpn_api')

# Stub urllib3 HTTPError
urllib3_mod = types.ModuleType('urllib3')
urllib3_exceptions = types.ModuleType('urllib3.exceptions')


class DummyHTTPError(Exception):
    pass


urllib3_exceptions.HTTPError = DummyHTTPError
urllib3_mod.exceptions = urllib3_exceptions
sys.modules['urllib3'] = urllib3_mod
sys.modules['urllib3.exceptions'] = urllib3_exceptions


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
models_mod.DescribeVpnGatewaysRequest = BaseReq
models_mod.DescribeVpnGatewaysResponse = Resp
models_mod.DescribeVpnGatewayRouteAttributesRequest = BaseReq
models_mod.DescribeVpnGatewayRouteAttributesResponse = Resp
models_mod.DescribeVpnGatewayRoutesRequest = BaseReq
models_mod.DescribeVpnGatewayRoutesResponse = Resp
models_mod.DescribeCustomerGatewaysRequest = BaseReq
models_mod.DescribeCustomerGatewaysResponse = Resp
models_mod.DescribeSslVpnClientCertAttributesRequest = BaseReq
models_mod.DescribeSslVpnClientCertAttributesResponse = Resp
sys.modules['volcenginesdkcore'] = core
sys.modules['volcenginesdkcore.rest'] = core.rest
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


class ToolAnnotations:
    def __init__(self, **kwargs):
        pass


types_mod.ToolAnnotations = ToolAnnotations
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
        from mcp_server_vpn.clients.models import DescribeVpnConnectionAttributesResponse
        return DescribeVpnConnectionAttributesResponse(Message="ok")

    def describe_vpn_gateways(self, req):
        if self.exc:
            raise self.exc
        from mcp_server_vpn.clients.models import DescribeVpnGatewaysResponse
        return DescribeVpnGatewaysResponse(Message="ok")

    def describe_vpn_gateway_route_attributes(self, req):
        if self.exc:
            raise self.exc
        from mcp_server_vpn.clients.models import (
            DescribeVpnGatewayRouteAttributesResponse,
        )
        return DescribeVpnGatewayRouteAttributesResponse(Message="ok")

    def describe_vpn_gateway_routes(self, req):
        if self.exc:
            raise self.exc
        from mcp_server_vpn.clients.models import DescribeVpnGatewayRoutesResponse
        return DescribeVpnGatewayRoutesResponse(Message="ok")

    def describe_customer_gateways(self, req):
        if self.exc:
            raise self.exc
        from mcp_server_vpn.clients.models import DescribeCustomerGatewaysResponse
        return DescribeCustomerGatewaysResponse(Message="ok")

    def describe_ssl_vpn_client_cert_attributes(self, req):
        if self.exc:
            raise self.exc
        from mcp_server_vpn.clients.models import (
            DescribeSslVpnClientCertAttributesResponse,
        )
        return DescribeSslVpnClientCertAttributesResponse(Message="ok")


def test_describe_vpn_connection_success(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient())
    result = asyncio.run(server.describe_vpn_connection('id'))
    assert result.Message == 'ok'


def test_describe_vpn_connection_error(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient(Exception('boom')))
    result = asyncio.run(server.describe_vpn_connection('id'))
    assert isinstance(result, CallToolResult) and result.isError


def test_get_vpn_client_missing_vars(monkeypatch):
    monkeypatch.delenv('VOLCENGINE_ACCESS_KEY', raising=False)
    monkeypatch.delenv('VOLCENGINE_SECRET_KEY', raising=False)
    monkeypatch.delenv('VOLCENGINE_REGION', raising=False)
    monkeypatch.setattr(server, '_read_sts', lambda: {})

    class DummyClient:
        def __init__(self, **kwargs):
            pass

    monkeypatch.setattr(server, 'VPNClient', DummyClient)
    server._CLIENT_CACHE = {}
    with pytest.raises(ValueError, match="Missing required credentials"):
        server._get_vpn_client()


def test_describe_vpn_connection_missing_creds(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: (_ for _ in ()).throw(ValueError('Missing required credentials')))
    result = asyncio.run(server.describe_vpn_connection('id'))
    assert isinstance(result, CallToolResult) and result.isError


def test_describe_vpn_gateways_success(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient())
    result = asyncio.run(server.describe_vpn_gateways())
    assert result.Message == 'ok'


def test_describe_vpn_gateways_error(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient(Exception('boom')))
    result = asyncio.run(server.describe_vpn_gateways())
    assert isinstance(result, CallToolResult) and result.isError


def test_describe_vpn_gateway_route_success(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient())
    result = asyncio.run(server.describe_vpn_gateway_route('id'))
    assert result.Message == 'ok'


def test_describe_vpn_gateway_route_error(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient(Exception('boom')))
    result = asyncio.run(server.describe_vpn_gateway_route('id'))
    assert isinstance(result, CallToolResult) and result.isError


def test_describe_vpn_gateway_routes_success(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient())
    result = asyncio.run(server.describe_vpn_gateway_routes())
    assert result.Message == 'ok'


def test_describe_vpn_gateway_routes_error(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient(Exception('boom')))
    result = asyncio.run(server.describe_vpn_gateway_routes())
    assert isinstance(result, CallToolResult) and result.isError


def test_describe_customer_gateways_success(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient())
    result = asyncio.run(server.describe_customer_gateways())
    assert result.Message == 'ok'


def test_describe_customer_gateways_error(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient(Exception('boom')))
    result = asyncio.run(server.describe_customer_gateways())
    assert isinstance(result, CallToolResult) and result.isError


def test_describe_ssl_vpn_client_cert_attributes_success(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient())
    result = asyncio.run(server.describe_ssl_vpn_client_cert_attributes('id'))
    assert result.Message == 'ok'


def test_describe_ssl_vpn_client_cert_attributes_error(monkeypatch):
    monkeypatch.setattr(server, '_get_vpn_client', lambda region=None: StubClient(Exception('boom')))
    result = asyncio.run(server.describe_ssl_vpn_client_cert_attributes('id'))
    assert isinstance(result, CallToolResult) and result.isError
