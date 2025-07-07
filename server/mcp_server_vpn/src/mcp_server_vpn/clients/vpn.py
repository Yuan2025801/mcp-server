import time

import volcenginesdkcore
from urllib3.exceptions import HTTPError
from volcenginesdkcore.rest import ApiException
from volcenginesdkvpn.api.vpn_api import VPNApi
from volcenginesdkvpn.models import (
    DescribeVpnConnectionAttributesRequest,
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnConnectionsRequest,
    DescribeVpnConnectionsResponse,
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
        session_token: str | None = None,
        timeout: int = 5,
        max_retries: int = 3,
        backoff: float = 0.5
    ):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if session_token is not None:
            configuration.session_token = session_token
        configuration.timeout = timeout
        configuration.backoff = backoff
        configuration.max_retries = max_retries
        if host is not None:
            configuration.host = host
        self._timeout = timeout
        self._backoff = backoff
        self._max_retries = max_retries
        self.client = VPNApi(volcenginesdkcore.ApiClient(configuration))

    def _call(self, fn, *args, **kwargs):
        kwargs["_request_timeout"] = (self._timeout, self._timeout)
        for i in range(1, self._max_retries + 1):
            try:
                return fn(*args, **kwargs)
            except (ApiException, HTTPError):
                if i == self._max_retries:
                    raise
                time.sleep(self._backoff * 2 ** (i - 1))

    def describe_vpn_connection_attributes(
        self, request: DescribeVpnConnectionAttributesRequest
    ) -> DescribeVpnConnectionAttributesResponse:
        return self._call(self.client.describe_vpn_connection_attributes, request)

    def describe_vpn_gateway_attributes(
        self, request: DescribeVpnGatewayAttributesRequest
    ) -> DescribeVpnGatewayAttributesResponse:
        return self._call(self.client.describe_vpn_gateway_attributes, request)

    def describe_vpn_connections(
        self, request: DescribeVpnConnectionsRequest
    ) -> DescribeVpnConnectionsResponse:
        return self._call(self.client.describe_vpn_connections, request)
