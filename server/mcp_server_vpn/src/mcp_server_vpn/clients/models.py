from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    """Generic response model allowing extra fields."""

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True


class DescribeVpnConnectionAttributesResponse(BaseResponseModel):
    pass


class DescribeVpnGatewayAttributesResponse(BaseResponseModel):
    pass


class DescribeVpnConnectionsResponse(BaseResponseModel):
    pass


class DescribeVpnGatewaysResponse(BaseResponseModel):
    pass


class DescribeVpnGatewayRouteAttributesResponse(BaseResponseModel):
    pass


class DescribeVpnGatewayRoutesResponse(BaseResponseModel):
    pass


class DescribeCustomerGatewaysResponse(BaseResponseModel):
    pass


class DescribeSslVpnClientCertAttributesResponse(BaseResponseModel):
    pass


class DescribeSslVpnClientCertsResponse(BaseResponseModel):
    pass
