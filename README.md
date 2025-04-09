# mcp-server-indexnow

> A Model Context Protocol server allowing URL indexing request via IndexNow

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp_server_indexnow*.

### Using make

Alternatively you can install `mcp_server_indexnow` using make:
```bash
make install
```

After installation, you can run it using:
```bash
make start
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

Using uvx
```json
"mcpServers": {
  "mcp_server_indexnow": {
    "command": "uvx",
    "args": ["mcp_server_indexnow"]
  }
}
```

Using docker
```json
"mcpServers": {
  "mcp_server_indexnow": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "mcp/mcp_server_indexnow"]
  }
}
```

### Configure for Zed

Add to your Zed settings.json:

Using uvx
```json
"context_servers": [
  "mcp_server_indexnow": {
    "command": "uvx",
    "args": ["mcp_server_indexnow"]
  }
],
```

Using make installation
```json
"context_servers": {
  "mcp_server_indexnow": {
    "command": "make",
    "args": ["start"]
  }
},
```

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:
```bash
make mcp_inspector
```

## Development

For development, you can use the following commands:

```bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint

# Format code
make format
```

## License

mcp-server-indexnow is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.