#!/usr/bin/env python3
"""
Wrapper script to run the MCP GLM Vision server
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import and run the server
if __name__ == "__main__":
    from mcp_server_glm_vision import mcp

    mcp.run()
