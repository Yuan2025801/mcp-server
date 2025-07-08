import time

import volcenginesdkcore
from urllib3.exceptions import HTTPError
from volcenginesdkcore.rest import ApiException
from volcenginesdkvpn.api.vpn_api import VPNApi
from volcenginesdkvpn.models import (
    DescribeVpnConnectionAttributesRequest,
    DescribeVpnConnectionsRequest,
    DescribeVpnGatewayAttributesRequest,
    DescribeVpnGatewaysRequest,
    DescribeVpnGatewayRouteAttributesRequest,
)

from .models import (
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnGatewayAttributesResponse,
    DescribeVpnConnectionsResponse,
    DescribeVpnGatewaysResponse,
    DescribeVpnGatewayRouteAttributesResponse,
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

    @staticmethod
    def _wrap(resp, model_cls):
        if hasattr(resp, "to_dict"):
            data = resp.to_dict()
        elif hasattr(resp, "model_dump"):
            data = resp.model_dump()
        elif isinstance(resp, dict):
            data = resp
        else:
            data = getattr(resp, "__dict__", {})
        return model_cls(**data)

    def describe_vpn_connection_attributes(
        self, request: DescribeVpnConnectionAttributesRequest
    ) -> DescribeVpnConnectionAttributesResponse:
        resp = self._call(self.client.describe_vpn_connection_attributes, request)
        return self._wrap(resp, DescribeVpnConnectionAttributesResponse)

    def describe_vpn_gateway_attributes(
        self, request: DescribeVpnGatewayAttributesRequest
    ) -> DescribeVpnGatewayAttributesResponse:
        resp = self._call(self.client.describe_vpn_gateway_attributes, request)
        return self._wrap(resp, DescribeVpnGatewayAttributesResponse)

    def describe_vpn_connections(
        self, request: DescribeVpnConnectionsRequest
    ) -> DescribeVpnConnectionsResponse:
        resp = self._call(self.client.describe_vpn_connections, request)
        return self._wrap(resp, DescribeVpnConnectionsResponse)

    def describe_vpn_gateways(
        self, request: DescribeVpnGatewaysRequest
    ) -> DescribeVpnGatewaysResponse:
        resp = self._call(self.client.describe_vpn_gateways, request)
        return self._wrap(resp, DescribeVpnGatewaysResponse)

    def describe_vpn_gateway_route_attributes(
        self, request: DescribeVpnGatewayRouteAttributesRequest
    ) -> DescribeVpnGatewayRouteAttributesResponse:
        resp = self._call(
            self.client.describe_vpn_gateway_route_attributes, request
        )
        return self._wrap(resp, DescribeVpnGatewayRouteAttributesResponse)
