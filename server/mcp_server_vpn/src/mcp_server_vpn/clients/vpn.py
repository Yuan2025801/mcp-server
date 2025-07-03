import volcenginesdkcore
from volcenginesdkvpn.api.vpn_api import VPNApi
from volcenginesdkvpn.models import (
    DescribeVpnConnectionAttributesRequest,
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnGatewayAttributesRequest,
    DescribeVpnGatewayAttributesResponse,
)


class VPNClient:
    """Simple wrapper around the volcenginesdk VPN client."""

    def __init__(
        self,
        region: str | None = None,
        ak: str | None = None,
        sk: str | None = None,
        host: str | None = None,
    ):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = VPNApi(volcenginesdkcore.ApiClient(configuration))

    def describe_vpn_connection_attributes(
        self, request: DescribeVpnConnectionAttributesRequest
    ) -> DescribeVpnConnectionAttributesResponse:
        """Query details of a specific IPsec connection."""
        return self.client.describe_vpn_connection_attributes(request)

    def describe_vpn_gateway_attributes(
        self, request: DescribeVpnGatewayAttributesRequest
    ) -> DescribeVpnGatewayAttributesResponse:
        """Query details of a specific VPN gateway."""
        return self.client.describe_vpn_gateway_attributes(request)
