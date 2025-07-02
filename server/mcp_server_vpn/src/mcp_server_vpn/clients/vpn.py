import volcenginesdkcore
from volcenginesdkvpn.api.vpn_api import VPNApi
from volcenginesdkvpn.models import (
    DescribeVpnConnectionAttributesRequest,
    DescribeVpnConnectionAttributesResponse,
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
        self, args: dict
    ) -> DescribeVpnConnectionAttributesResponse:
        """Query details of a specific IPsec connection."""
        request = DescribeVpnConnectionAttributesRequest(**args)
        return self.client.describe_vpn_connection_attributes(request)
