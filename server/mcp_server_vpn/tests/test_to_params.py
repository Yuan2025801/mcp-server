import os
import sys
import types

# Stub minimal volcengine modules so BaseApi can be imported without the SDK
ve_mod = types.ModuleType('volcengine')
api_info_mod = types.ModuleType('volcengine.ApiInfo')
credentials_mod = types.ModuleType('volcengine.Credentials')
service_info_mod = types.ModuleType('volcengine.ServiceInfo')
base_service_mod = types.ModuleType('volcengine.base.Service')

class DummyService:
    def __init__(self, *a, **kw):
        pass

    def get(self, *a, **kw):
        return '{}'

api_info_mod.ApiInfo = object
credentials_mod.Credentials = object
service_info_mod.ServiceInfo = object
base_service_mod.Service = DummyService
base_mod = types.ModuleType('volcengine.base')
base_mod.Service = base_service_mod

ve_mod.Credentials = credentials_mod
ve_mod.ServiceInfo = service_info_mod

sys.modules['volcengine'] = ve_mod
sys.modules['volcengine.ApiInfo'] = api_info_mod
sys.modules['volcengine.Credentials'] = credentials_mod
sys.modules['volcengine.ServiceInfo'] = service_info_mod
sys.modules['volcengine.base'] = base_mod
sys.modules['volcengine.base.Service'] = base_service_mod

# Stub minimal vpn sdk modules used when importing the clients package
vpn_mod = types.ModuleType('volcenginesdkvpn')
vpn_api_mod = types.ModuleType('volcenginesdkvpn.api.vpn_api')
models_mod = types.ModuleType('volcenginesdkvpn.models')
sys.modules['volcenginesdkvpn'] = vpn_mod
sys.modules['volcenginesdkvpn.api'] = types.ModuleType('api')
sys.modules['volcenginesdkvpn.api.vpn_api'] = vpn_api_mod
sys.modules['volcenginesdkvpn.models'] = models_mod

# Provide dummy request/response classes to satisfy imports in vpn.py
for name in [
    'DescribeVpnConnectionAttributesRequest',
    'DescribeVpnConnectionsRequest',
    'DescribeVpnGatewayAttributesRequest',
    'DescribeVpnGatewaysRequest',
    'DescribeVpnGatewayRouteAttributesRequest',
    'DescribeVpnGatewayRoutesRequest',
    'DescribeCustomerGatewaysRequest',
    'DescribeSslVpnClientCertAttributesRequest',
    'DescribeSslVpnClientCertsRequest',
    'DescribeSslVpnServersRequest',
]:
    setattr(models_mod, name, object)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from mcp_server_vpn.clients.base import BaseApi

class DummyRequest:
    attribute_map = {"vpn_connection_id": "VpnConnectionId", "region": "Region"}

    def __init__(self, vpn_connection_id: str, region: str | None = None):
        self.vpn_connection_id = vpn_connection_id
        self.region = region

    def to_dict(self):
        return {
            "vpn_connection_id": self.vpn_connection_id,
            "region": self.region,
        }


def test_to_params_applies_attribute_map():
    req = DummyRequest("vpc-123", None)
    params = BaseApi.to_params(req)
    assert params == {"VpnConnectionId": "vpc-123"}
