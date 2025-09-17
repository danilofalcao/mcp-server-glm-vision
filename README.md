# MCP Server GLM Vision

A Model Context Protocol (MCP) server that integrates GLM-4.5V from Z.AI with Claude Code.

## Features

- **Image Analysis**: Analyze images using GLM-4.5V's vision capabilities
- **Local File Support**: Analyze local image files or URLs
- **Configurable**: Easy setup with environment variables

## Installation

### Prerequisites

- Python 3.10 or higher
- GLM API key from Z.AI
- Claude Code installed

### Setup

1. **Clone or create the project directory:**
   ```bash
   cd /path/to/your/project
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or with uv (recommended)
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your GLM API key from Z.AI
   ```

5. **Add the server to Claude Code:**
   ```bash
   # Using uv (recommended)
   uv run mcp install -e . --name "GLM Vision Server"

   # Or manually add to Claude Desktop configuration:
   claude mcp add-json --scope user glm-vision '{
     "type": "stdio",
     "command": "/path/to/your/project/env/bin/python",
     "args": ["/path/to/your/project/glm-vision.py"],
     "env": {"GLM_API_KEY": "your_api_key_here"}
   }'
   ```

## Configuration

Set these environment variables in your `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `GLM_API_KEY` | Your GLM API key from Z.AI | (required) |
| `GLM_API_BASE` | GLM API base URL | `https://api.z.ai/api/paas/v4` |
| `GLM_MODEL` | Model name to use | `glm-4.5v` |

## Usage

### Available Tools

#### `glm-vision`
Analyze an image file using GLM-4.5V's vision capabilities. Supports both local files and URLs.

**Parameters:**
- `image_path` (required): Local file path or URL of the image to analyze
- `prompt` (required): What to ask about the image
- `temperature` (optional): Response randomness (0.0-1.0, default: 0.7)
- `thinking` (optional): Enable thinking mode to see model's reasoning process (default: false)
- `max_tokens` (optional): Maximum tokens in response (max 64K, default: 2048)

**Example:**
```
Use the glm-vison tool with:
- image_path: "/path/to/your/image.jpg"
- prompt: "Describe what you see in this image"
```

### Testing

Test the server using the MCP Inspector:

```bash
# With uv
uv run python glm-vision.py

# Or with python
python glm-vision.py
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy glm-vision.py
```

### Troubleshooting

1. **API Key Issues**: Make sure your `GLM_API_KEY` is correctly set in the environment
2. **Connection Problems**: Check your internet connection and API endpoint
3. **Model Errors**: Verify that the model name (`GLM_MODEL`) is correct and available

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues related to the GLM API, contact Z.AI support.
For MCP server issues, please create an issue in the repository.
