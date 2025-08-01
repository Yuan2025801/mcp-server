import os
from dataclasses import dataclass
import logging
from typing import Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ENV_ASK_ECHO_SEARCH_INFINITY_API_KEY = "ASK_ECHO_SEARCH_INFINITY_API_KEY"
ENV_VOLCENGINE_ACCESS_KEY = "VOLCENGINE_ACCESS_KEY"
ENV_VOLCENGINE_SECRET_KEY = "VOLCENGINE_SECRET_KEY"


@dataclass
class SearchInfinityConfig:
    api_key: Optional[str] = None
    volcengine_ak: Optional[str] = None
    volcengine_sk: Optional[str] = None


def load_config() -> SearchInfinityConfig:
    """Load configuration from environment variables."""
    try:
        """Load Authentication environment variable: API KEY or VOLCENGINE AK SK"""
        api_key = os.environ.get(ENV_ASK_ECHO_SEARCH_INFINITY_API_KEY)
        volcengine_ak = os.environ.get(ENV_VOLCENGINE_ACCESS_KEY)
        volcengine_sk = os.environ.get(ENV_VOLCENGINE_SECRET_KEY)
        has_api_key_auth = api_key is not None and len(api_key) > 0
        has_volcengine_auth = volcengine_ak is not None and len(
            volcengine_ak) > 0 and volcengine_sk is not None and len(volcengine_sk) > 0
        if not (has_api_key_auth or has_volcengine_auth):
            missing_auth = []
            if not has_api_key_auth:
                missing_auth.append(ENV_ASK_ECHO_SEARCH_INFINITY_API_KEY)
            if not has_volcengine_auth:
                missing_volc = []
                if volcengine_ak is None:
                    missing_volc.append(ENV_VOLCENGINE_ACCESS_KEY)
                if volcengine_sk is None:
                    missing_volc.append(ENV_VOLCENGINE_SECRET_KEY)
                missing_auth.append(
                    f"either both {ENV_VOLCENGINE_ACCESS_KEY} and {ENV_VOLCENGINE_SECRET_KEY} or neither")
            raise ValueError(
                f"Authentication missing. Must provide either {ENV_ASK_ECHO_SEARCH_INFINITY_API_KEY} "
                f"or both {ENV_VOLCENGINE_ACCESS_KEY} and {ENV_VOLCENGINE_SECRET_KEY}. "
                f"Missing: {', '.join(missing_auth)}"
            )
        logger.info(f"Loaded configuration: Using {'API Key' if has_api_key_auth else 'VOLCENGINE AK SK'}")
        return SearchInfinityConfig(
            api_key=api_key,
            volcengine_ak=volcengine_ak,
            volcengine_sk=volcengine_sk,
        )
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise