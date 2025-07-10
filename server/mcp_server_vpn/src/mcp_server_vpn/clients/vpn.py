from volcengine.ApiInfo import ApiInfo

from typing import Any

from .base import BaseApi
from .models import (
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnGatewayAttributesResponse,
    DescribeVpnConnectionsResponse,
    DescribeVpnGatewaysResponse,
    DescribeVpnGatewayRouteAttributesResponse,
    DescribeVpnGatewayRoutesResponse,
    DescribeCustomerGatewaysResponse,
    DescribeSslVpnClientCertAttributesResponse,
    DescribeSslVpnClientCertsResponse,
    DescribeSslVpnServersResponse,
)


class VPNClient(BaseApi):
    """VPN client implemented using BaseApi."""

    def __init__(self, region: str, endpoint: str, ak: str, sk: str) -> None:
        api_infos = {
            "DescribeVpnConnectionAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnConnectionAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGatewayAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGatewayAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnConnections": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnConnections", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGateways": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGateways", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGatewayRouteAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGatewayRouteAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGatewayRoutes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGatewayRoutes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeCustomerGateways": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeCustomerGateways", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeSslVpnClientCertAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeSslVpnClientCertAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeSslVpnClientCerts": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeSslVpnClientCerts", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeSslVpnServers": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeSslVpnServers", "Version": "2020-04-01"},
                {},
                {},
            ),
        }
        self.region = region
        super().__init__(region, endpoint, api_infos, "vpc", ak, sk)


    def describe_vpn_connection_attributes(
        self, vpn_connection_id: str
    ) -> DescribeVpnConnectionAttributesResponse:
        params = {"VpnConnectionId": vpn_connection_id}
        data = self.get("DescribeVpnConnectionAttributes", params)
        return DescribeVpnConnectionAttributesResponse(**data)

    def describe_vpn_gateway_attributes(
        self, vpn_gateway_id: str
    ) -> DescribeVpnGatewayAttributesResponse:
        params = {"VpnGatewayId": vpn_gateway_id}
        data = self.get("DescribeVpnGatewayAttributes", params)
        return DescribeVpnGatewayAttributesResponse(**data)

    def describe_vpn_connections(
        self,
        page_number: int | None = None,
        page_size: int | None = None,
        vpn_gateway_id: str | None = None,
        vpn_connection_name: str | None = None,
        status: str | None = None,
    ) -> DescribeVpnConnectionsResponse:
        raw_params: dict[str, Any] = {
            "PageNumber": page_number,
            "PageSize": page_size,
            "VpnGatewayId": vpn_gateway_id,
            "VpnConnectionName": vpn_connection_name,
            "Status": status,
        }
        params = {k: v for k, v in raw_params.items() if v is not None}
        data = self.get("DescribeVpnConnections", params)
        return DescribeVpnConnectionsResponse(**data)

    def describe_vpn_gateways(
        self,
        page_number: int | None = None,
        page_size: int | None = None,
        ip_address: str | None = None,
        ssl_enabled: bool | None = None,
        subnet_id: str | None = None,
        vpc_id: str | None = None,
        vpn_gateway_name: str | None = None,
        ipsec_enabled: bool | None = None,
        project_name: str | None = None,
        vpn_gateway_ids: list[str] | None = None,
        tag_filters: list[dict] | None = None,
    ) -> DescribeVpnGatewaysResponse:
        raw_params: dict[str, Any] = {
            "PageNumber": page_number,
            "PageSize": page_size,
            "IpAddress": ip_address,
            "SslEnabled": ssl_enabled,
            "SubnetId": subnet_id,
            "VpcId": vpc_id,
            "VpnGatewayName": vpn_gateway_name,
            "IpsecEnabled": ipsec_enabled,
            "ProjectName": project_name,
            "VpnGatewayIds": vpn_gateway_ids,
            "TagFilters": tag_filters,
        }
        params = {k: v for k, v in raw_params.items() if v is not None}
        data = self.get("DescribeVpnGateways", params)
        return DescribeVpnGatewaysResponse(**data)

    def describe_vpn_gateway_route_attributes(
        self, vpn_gateway_route_id: str
    ) -> DescribeVpnGatewayRouteAttributesResponse:
        params = {"VpnGatewayRouteId": vpn_gateway_route_id}
        data = self.get("DescribeVpnGatewayRouteAttributes", params)
        return DescribeVpnGatewayRouteAttributesResponse(**data)

    def describe_vpn_gateway_routes(
        self,
        page_number: int | None = None,
        page_size: int | None = None,
        destination_cidr_block: str | None = None,
        next_hop_id: str | None = None,
        route_type: str | None = None,
        status: str | None = None,
        vpn_gateway_id: str | None = None,
        vpn_gateway_route_ids: list[str] | None = None,
    ) -> DescribeVpnGatewayRoutesResponse:
        raw_params: dict[str, Any] = {
            "PageNumber": page_number,
            "PageSize": page_size,
            "DestinationCidrBlock": destination_cidr_block,
            "NextHopId": next_hop_id,
            "RouteType": route_type,
            "Status": status,
            "VpnGatewayId": vpn_gateway_id,
            "VpnGatewayRouteIds": vpn_gateway_route_ids,
        }
        params = {k: v for k, v in raw_params.items() if v is not None}
        data = self.get("DescribeVpnGatewayRoutes", params)
        return DescribeVpnGatewayRoutesResponse(**data)

    def describe_customer_gateways(
        self,
        page_number: int | None = None,
        page_size: int | None = None,
        customer_gateway_name: str | None = None,
        ip_address: str | None = None,
        status: str | None = None,
        tag_filters: list[dict] | None = None,
        project_name: str | None = None,
        customer_gateway_ids: list[str] | None = None,
    ) -> DescribeCustomerGatewaysResponse:
        raw_params: dict[str, Any] = {
            "PageNumber": page_number,
            "PageSize": page_size,
            "CustomerGatewayName": customer_gateway_name,
            "IpAddress": ip_address,
            "Status": status,
            "TagFilters": tag_filters,
            "ProjectName": project_name,
            "CustomerGatewayIds": customer_gateway_ids,
        }
        params = {k: v for k, v in raw_params.items() if v is not None}
        data = self.get("DescribeCustomerGateways", params)
        return DescribeCustomerGatewaysResponse(**data)

    def describe_ssl_vpn_client_cert_attributes(
        self, ssl_vpn_client_cert_id: str
    ) -> DescribeSslVpnClientCertAttributesResponse:
        params = {"SslVpnClientCertId": ssl_vpn_client_cert_id}
        data = self.get("DescribeSslVpnClientCertAttributes", params)
        return DescribeSslVpnClientCertAttributesResponse(**data)

    def describe_ssl_vpn_client_certs(
        self,
        page_number: int | None = None,
        page_size: int | None = None,
        ssl_vpn_client_cert_ids: list[str] | None = None,
        ssl_vpn_client_cert_name: str | None = None,
        ssl_vpn_server_id: str | None = None,
        tag_filters: list[dict] | None = None,
    ) -> DescribeSslVpnClientCertsResponse:
        raw_params: dict[str, Any] = {
            "PageNumber": page_number,
            "PageSize": page_size,
            "SslVpnClientCertIds": ssl_vpn_client_cert_ids,
            "SslVpnClientCertName": ssl_vpn_client_cert_name,
            "SslVpnServerId": ssl_vpn_server_id,
            "TagFilters": tag_filters,
        }
        params = {k: v for k, v in raw_params.items() if v is not None}
        data = self.get("DescribeSslVpnClientCerts", params)
        return DescribeSslVpnClientCertsResponse(**data)

    def describe_ssl_vpn_servers(
        self,
        page_number: int | None = None,
        page_size: int | None = None,
        project_name: str | None = None,
        tag_filters: list[dict] | None = None,
        vpn_gateway_id: str | None = None,
        ssl_vpn_server_name: str | None = None,
        ssl_vpn_server_ids: list[str] | None = None,
    ) -> DescribeSslVpnServersResponse:
        raw_params: dict[str, Any] = {
            "PageNumber": page_number,
            "PageSize": page_size,
            "ProjectName": project_name,
            "TagFilters": tag_filters,
            "VpnGatewayId": vpn_gateway_id,
            "SslVpnServerName": ssl_vpn_server_name,
            "SslVpnServerIds": ssl_vpn_server_ids,
        }
        params = {k: v for k, v in raw_params.items() if v is not None}
        data = self.get("DescribeSslVpnServers", params)
        return DescribeSslVpnServersResponse(**data)
