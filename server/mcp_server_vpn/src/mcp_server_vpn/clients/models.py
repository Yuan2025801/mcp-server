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
