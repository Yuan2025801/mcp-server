# VPN MCP Server

| Version | v1.0.0 |
| ------- | ------ |
| Description | Manage VPN gateways and IPsec connections using natural language |
| Category | Networking |

The VPN MCP Server enables natural language access to Volcengine VPN resources, including gateways, connections and SSL VPN servers.

## Tools

- `describe_vpn_connection`：查询指定的 IPsec 连接详情。
- `describe_vpn_gateway`：查询指定的 VPN 网关详情。
- `describe_vpn_connections`：查询满足条件的 IPsec 连接列表。
- `describe_vpn_gateways`：查询满足条件的 VPN 网关列表。
- `describe_vpn_gateway_route`：查询指定的 VPN 网关路由条目详情。
- `describe_vpn_gateway_routes`：查询满足条件的 VPN 网关路由条目列表。
- `describe_customer_gateways`：查询满足条件的用户网关列表。
- `describe_ssl_vpn_client_cert_attributes`：查询指定的 SSL 客户端证书详情。
- `describe_ssl_vpn_servers`：查询满足条件的 SSL 服务端列表。

## Compatible Platforms

This server can be used with Ark, Cursor, Claude Desktop and any other MCP client that supports custom servers.

## Installation

### System requirements
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv
**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Usage
Install the dependencies with `uv` and run the server:

```bash
uv run mcp-server-vpn
```

To use SSE transport:
```bash
uv run mcp-server-vpn -t sse
```


## MCP Integration

To add this server to your MCP configuration, add the following to your MCP settings file:

```json
{
  "mcpServers": {
    "mcp-server-vpn": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vpn",
        "mcp-server-vpn"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "your-resource-region",
        "VOLCENGINE_ENDPOINT": "api-endpoint",
        "PORT": "8000"
      }
    }
  }
}

```

### 环境变量

| 环境变量 | 描述 | 必填 | 默认值 |
| --- | --- | --- | --- |
| VOLCENGINE_ENDPOINT | 火山引擎 OpenAPI Endpoint | 否 | - |
| VOLCENGINE_REGION | 火山引擎 VortexIP Region | 是 | - |
| VOLCENGINE_ACCESS_KEY | 火山引擎账号 ACCESS KEY | 是 | - |
| VOLCENGINE_SECRET_KEY | 火山引擎账号 SECRET KEY | 是 | - |

## License

volcengine/mcp-server is licensed under the MIT License.
