
# VPN MCP Server

Skeleton MCP server for VPN related tools. Functionality will be added in future versions.

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

## License

volcengine/mcp-server is licensed under the MIT License.
