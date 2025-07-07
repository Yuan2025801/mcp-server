# VPN MCP Server

Skeleton MCP server for VPN related tools. Functionality will be added in future versions.

## Tools

### `describe_vpn_connection`

- **详细描述**：查询指定的 IPsec 连接详情。
- **触发示例**：`"查看 IPsec 连接 vpn-123 的状态"`


### `describe_vpn_gateway`

- **详细描述**：查询指定的 VPN 网关详情。
- **触发示例**：`"查看 VPN 网关 vgw-123 的状态"`

### `describe_vpn_connections`

- **详细描述**：查询满足条件的 IPsec 连接列表。
- **触发示例**：`"列出所有 IPsec 连接"`

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

## Debugging (Command Line)

The following steps demonstrate how to simulate APIG using MCP Inspector and verify the server:

1. Install [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector).

2. Prepare STS information in the JSON structure below and convert it to a base64 string:

```json
{
  "CurrentTime": "2021-04-12T10:57:09+08:00",
  "ExpiredTime": "2021-04-12T11:57:09+08:00",
  "AccessKeyId": "ak",
  "SecretAccessKey": "sk",
  "SessionToken": ""
}
```

3. Start the server in **STDIO mode**. The script below sets the base64 `authorization` environment variable and launches the server via MCP Inspector:

```bash
#!/usr/bin/env bash
auth_json='{"AccessKeyId":"ak","SecretAccessKey":"sk","SessionToken":""}'
export authorization=$(echo -n "$auth_json" | base64)
npx @modelcontextprotocol/inspector \
  python -m mcp_server_vpn.main -t stdio
```

4. For **SSE mode**, run the inspector and the server separately:

```bash
npx @modelcontextprotocol/inspector sleep 9999
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
