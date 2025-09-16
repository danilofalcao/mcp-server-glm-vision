#!/usr/bin/env python3
"""
MCP Server for GLM Vision integration with Claude Code
This server provides access to GLM-4.5V model from Z.AI
"""

import base64
import mimetypes
import os
from typing import Any, Dict, List, Optional, cast

import httpx
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("GLM Vision Server")

# Configuration
GLM_API_BASE = os.environ.get("GLM_API_BASE", "https://api.z.ai/api/paas/v4")
GLM_API_KEY = os.environ.get("GLM_API_KEY", "")
GLM_MODEL = os.environ.get("GLM_MODEL", "glm-4.5v")


class GLMClient:
    """Client for interacting with GLM-4.5V API"""

    def __init__(self, api_key: str, base_url: str = GLM_API_BASE):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    def encode_image(self, image_path: str) -> Dict[str, str]:
        """Encode local image file to base64"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith("image/"):
            raise ValueError(f"Unsupported file type: {mime_type}")

        # Read and encode image
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        return {"mime_type": mime_type, "data": encoded_string}

    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: str = GLM_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        thinking: bool = False,
    ) -> Dict[str, Any]:
        """Send chat completion request to GLM API"""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        # Add thinking mode if enabled
        if thinking:
            payload["thinking"] = {"type": "enabled"}

        response = await self.client.post("/chat/completions", json=payload)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    async def analyze_image(
        self,
        image_path: str,
        prompt: str,
        model: str = GLM_MODEL,
        temperature: float = 0.7,
        thinking: bool = False,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """Analyze local image file using GLM-4.5V"""
        # Check if it's a URL or local file
        if image_path.startswith(("http://", "https://")):
            # It's a URL
            content = [
                {"type": "image_url", "image_url": {"url": image_path}},
                {"type": "text", "text": prompt},
            ]
        else:
            # It's a local file
            encoded_image = self.encode_image(image_path)
            content = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{encoded_image['mime_type']};base64,{encoded_image['data']}"
                    },
                },
                {"type": "text", "text": prompt},
            ]

        messages = [{"role": "user", "content": content}]
        return await self.chat_completion(
            messages,
            model,
            temperature=temperature,
            thinking=thinking,
            max_tokens=max_tokens,
        )

    async def close(self) -> None:
        """Close the HTTP client"""
        await self.client.aclose()


# Global GLM client instance
glm_client: Optional[GLMClient] = None

# Initialize GLM client if API key is provided
if GLM_API_KEY:
    glm_client = GLMClient(GLM_API_KEY, GLM_API_BASE)


@mcp.tool()
async def glm_vision(
    image_path: str,
    prompt: str,
    temperature: float = 0.7,
    thinking: bool = False,
    max_tokens: int = 2048,
) -> str:
    """Analyze an image file using GLM-4.5V's vision capabilities. Supports both local files and URLs."""
    if not glm_client:
        return "Error: GLM client not initialized. Please check your API key."

    try:
        response = await glm_client.analyze_image(
            image_path=image_path,
            prompt=prompt,
            temperature=temperature,
            thinking=thinking,
            max_tokens=max_tokens,
        )

        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            return str(content)
        else:
            return "No response from GLM model"

    except httpx.HTTPStatusError as e:
        return f"GLM API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Run the server
    if not GLM_API_KEY:
        print("Warning: GLM_API_KEY environment variable not set. Tools will not work.")
    mcp.run()
