# VPN MCP Server

Skeleton MCP server for VPN related tools. Functionality will be added in future versions.

## Prerequisites
- Python 3.10+
- [UV](https://github.com/astral-sh/uv)

## Installation
Clone the repository:
```bash
git clone git@github.com:volcengine/mcp-server.git
```

## Usage
Start the server:

```bash
cd mcp-server/server/mcp_server_vpn
uv run mcp-server-vpn

# Start with sse mode (default is stdio)
uv run mcp-server-vpn -t sse
```

## Configuration
### Environment Variables
| Environment Variable | Description | Default Value |
|----------------------|-------------|---------------|
| `PORT` | VPN MCP Server listening port | `8000` |

Example:
```bash
export PORT=8000
```

## License

volcengine/mcp-server is licensed under the MIT License.
