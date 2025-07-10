import json

from volcengine.ApiInfo import ApiInfo
from typing import Any
from volcengine import Credentials
from volcengine import ServiceInfo
from volcengine.base import Service


class BaseApi(Service.Service):
    def __init__(self, region, endpoint, api_info, service, ak, sk):
        """init function.
        :param region:   region of request
        :param api_info: an object of volcengine.ApiInfo.ApiInfo()
        :param endpoint: endpoint of top gateway
        :param service:  a specific service name registered on top gateway
        :param ak:       account ak
        :param sk:       account ak
        """
        self.connection_timeout = 10
        self.socket_timeout = 10
        self.schema = 'https'
        self.header = dict()
        self.header["Content-Type"] = "application/json"
        self.endpoint = endpoint

        self.credential = Credentials.Credentials(ak, sk, service, region)
        self.service_info = ServiceInfo.ServiceInfo(
            self.endpoint,
            self.header,
            self.credential,
            self.connection_timeout,
            self.socket_timeout,
            self.schema,
        )
        self.api_info = api_info
        Service.Service.__init__(self, self.service_info, self.api_info)

    @staticmethod
    def to_params(obj: Any) -> dict[str, Any]:
        """Convert a request model to a parameters dict, dropping None values."""
        if hasattr(obj, "to_dict"):
            data = obj.to_dict()
        elif hasattr(obj, "model_dump"):
            data = obj.model_dump()
        elif isinstance(obj, dict):
            data = obj
        else:
            data = getattr(obj, "__dict__", {})
        return {k: v for k, v in data.items() if v is not None}

    def get(self, action, params, doseq=0):
        res = super(BaseApi, self).get(action, params, doseq)
        try:
            res_json = json.loads(res)
        except Exception as e:
            raise Exception("res body is not json, %s, %s" % (e, res))
        if "ResponseMetadata" not in res_json:
            raise Exception(
                "ResponseMetadata not in resp body, action %s, resp %s" % (action, res)
            )
        elif "Error" in res_json["ResponseMetadata"]:
            raise Exception("%s failed, %s" % (action, res))
        return res_json
