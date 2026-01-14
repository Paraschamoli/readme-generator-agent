# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""readme-generator-agent - An Bindu Agent."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.openrouter import OpenRouter
from agno.tools.github import GithubTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.mem0 import Mem0Tools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global agent instance
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


def load_config() -> dict:
    """Load agent configuration from project root."""
    # Try multiple possible locations for agent_config.json
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except (PermissionError, json.JSONDecodeError) as e:
                print(f"⚠️  Error reading {config_path}: {type(e).__name__}")
                continue
            except Exception as e:
                print(f"⚠️  Unexpected error reading {config_path}: {type(e).__name__}")
                continue

    # If no config found or readable, create a minimal default
    print("⚠️  No agent_config.json found, using default configuration")
    return {
        "name": "readme-generator-agent",
        "description": "AI-powered README generator that creates comprehensive, professional documentation for open source projects by analyzing GitHub repositories",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {"key": "OPENAI_API_KEY", "description": "OpenAI API key for LLM calls", "required": False},
            {"key": "OPENROUTER_API_KEY", "description": "OpenRouter API key for LLM calls", "required": False},
            {
                "key": "GITHUB_ACCESS_TOKEN",
                "description": "GitHub personal access token for repository access",
                "required": False,
            },
            {"key": "MEM0_API_KEY", "description": "Mem0 API key for memory operations", "required": False},
        ],
    }


async def initialize_agent() -> None:
    """Initialize the README generator agent with proper model and tools."""
    global agent

    # Get API keys from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    mem0_api_key = os.getenv("MEM0_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")

    # Model selection logic
    if openai_api_key:
        model = OpenAIChat(id="gpt-4o", api_key=openai_api_key)
        print("✅ Using OpenAI GPT-4o")
    elif openrouter_api_key:
        model = OpenRouter(
            id=model_name,
            api_key=openrouter_api_key,
            cache_response=True,
            supports_native_structured_outputs=True,
        )
        print(f"✅ Using OpenRouter model: {model_name}")
    else:
        error_msg = (
            "No API key provided. Set OPENAI_API_KEY or OPENROUTER_API_KEY environment variable.\n"
            "For OpenRouter: https://openrouter.ai/keys\n"
            "For OpenAI: https://platform.openai.com/api-keys"
        )
        raise ValueError(error_msg)

    # Initialize tools
    tools = []

    # Add GitHub tools if access token is available
    if github_access_token:
        github_tools = GithubTools(access_token=github_access_token)
        tools.append(github_tools)
        print("✅ Added GitHub repository tools")
    else:
        print("⚠️  GITHUB_ACCESS_TOKEN not set - GitHub repository access disabled")
        print("i  Get a token from: https://github.com/settings/tokens")

    # Add local file system tools (always available)
    filesystem_tools = LocalFileSystemTools()
    tools.append(filesystem_tools)
    print("✅ Added local file system tools")

    # Add Mem0 if available
    if mem0_api_key:
        mem0_tools = Mem0Tools(api_key=mem0_api_key)
        tools.append(mem0_tools)
        print("✅ Added Mem0 memory tools")
    else:
        print("⚠️  MEM0_API_KEY not set - memory features disabled")

    # Create the README generator agent
    agent = Agent(
        name="README Generator",
        model=model,
        tools=tools,
        description=dedent("""\
            You are an intelligent automation tool that creates comprehensive,
            professional README files for open source projects. Your expertise encompasses: 📄

            - GitHub repository analysis and documentation extraction
            - Professional README structure and formatting
            - Badge generation and integration
            - Installation and usage instructions
            - Contribution guidelines and documentation
            - License information and compliance
            - Project metadata and description crafting
        """),
        instructions=dedent("""\
            **README GENERATION PROTOCOL:**

            1. **Repository Analysis**:
               - Extract owner/repo_name from provided URL or repository name
               - Use `get_repository` tool with format: owner/repo_name
               - Call `get_repository_languages` to analyze technology stack
               - Gather repository metadata, description, and structure

            2. **Content Generation**:
               - Create comprehensive README with professional structure
               - Include project title and clear description
               - Add relevant badges (license, size, version, etc.)
               - Document installation and setup procedures
               - Provide usage examples and API documentation
               - Include contribution guidelines
               - Add license information

            3. **Formatting Standards**:
               - Use proper Markdown formatting
               - Include table of contents for large READMEs
               - Add code blocks with appropriate language highlighting
               - Use consistent heading hierarchy
               - Include links to related resources

            4. **Quality Assurance**:
               - Verify all information is accurate and up-to-date
               - Ensure instructions are clear and actionable
               - Check for broken links or missing information
               - Maintain professional tone and style

            **SPECIFIC REQUIREMENTS:**
            - DO NOT include the project's languages-used section in the README
            - DO include badges for license, repository size, version, etc.
            - DO write the produced README to the local filesystem
            - DO provide clear cloning and installation instructions
            - DO include how to run the project with examples

            **TOOL USAGE:**
            - GitHub Tools: For repository analysis and metadata extraction
            - File System Tools: For writing README to local filesystem
            - Memory Tools: For context retention across sessions (if available)

            **OUTPUT FORMAT:**
            - Professional-grade README.md file
            - Well-structured with clear sections
            - Proper Markdown formatting
            - Ready for immediate use in projects

            Remember: Your READMEs are often the first impression of a project.
            Make them comprehensive, professional, and useful.
        """),
        expected_output=dedent("""\
            # Generated README.md Structure 📄

            ## Project Title
            {Concise, descriptive project name}

            ## Badges
            [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
            [![GitHub repo size](https://img.shields.io/github/repo-size/{owner}/{repo})](https://github.com/{owner}/{repo})
            [![GitHub stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social)](https://github.com/{owner}/{repo}/stargazers)

            ## Description
            {Clear, comprehensive project description explaining what it does, why it exists, and who it's for}

            ## Table of Contents
            - [Installation](#installation)
            - [Usage](#usage)
            - [Features](#features)
            - [Configuration](#configuration)
            - [Contributing](#contributing)
            - [License](#license)
            - [Contact](#contact)

            ## Installation
            ```bash
            # Clone the repository
            git clone https://github.com/{owner}/{repo}.git
            cd {repo}

            # Install dependencies
            {appropriate installation commands based on project type}
            ```

            ## Usage
            ```{language}
            {Example code showing basic usage}
            ```

            ## Features
            - {Feature 1 with description}
            - {Feature 2 with description}
            - {Feature 3 with description}

            ## Configuration
            {Environment variables, configuration files, or settings}

            ## API Documentation
            {If applicable, API endpoints and usage}

            ## Contributing
            {Guidelines for contributing, pull request process, code standards}

            ## License
            This project is licensed under the {License Name} License - see the [LICENSE](LICENSE) file for details.

            ## Contact
            - Project Link: [https://github.com/{owner}/{repo}](https://github.com/{owner}/{repo})
            - Issues: [GitHub Issues](https://github.com/{owner}/{repo}/issues)

            ## Acknowledgments
            {References, inspirations, or thanks}

            ---
            README generated by AI README Generator Agent
            Professional Documentation Automation Tool
            Generated: {current_date}
            Last Updated: {current_time}
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
    print("✅ README Generator Agent initialized")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent
    if not agent:
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    # Run the agent and get response
    response = await agent.arun(messages)
    return response


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    # Lazy initialization on first call
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing README Generator Agent...")
            await initialize_agent()
            _initialized = True

    # Run the async agent
    result = await run_agent(messages)
    return result


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up README Generator Agent resources...")


def main():
    """Run the main entry point for the README Generator Agent."""
    parser = argparse.ArgumentParser(description="Bindu README Generator Agent")
    parser.add_argument(
        "--openai-api-key",
        type=str,
        default=os.getenv("OPENAI_API_KEY"),
        help="OpenAI API key (env: OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--github-access-token",
        type=str,
        default=os.getenv("GITHUB_ACCESS_TOKEN"),
        help="GitHub personal access token (env: GITHUB_ACCESS_TOKEN)",
    )
    parser.add_argument(
        "--mem0-api-key",
        type=str,
        default=os.getenv("MEM0_API_KEY"),
        help="Mem0 API key (env: MEM0_API_KEY)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-4o"),
        help="Model ID for OpenRouter (env: MODEL_NAME)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to agent_config.json (optional)",
    )
    args = parser.parse_args()

    # Set environment variables if provided via CLI
    if args.openai_api_key:
        os.environ["OPENAI_API_KEY"] = args.openai_api_key
    if args.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_api_key
    if args.github_access_token:
        os.environ["GITHUB_ACCESS_TOKEN"] = args.github_access_token
    if args.mem0_api_key:
        os.environ["MEM0_API_KEY"] = args.mem0_api_key
    if args.model:
        os.environ["MODEL_NAME"] = args.model

    print("🤖 README Generator Agent - AI Documentation Automation")
    print("📄 Capabilities: GitHub repository analysis, professional README generation, badge creation")

    # Load configuration
    config = load_config()

    try:
        # Bindufy and start the agent server
        print("🚀 Starting Bindu README Generator Agent server...")
        print(f"🌐 Server will run on: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 README Generator Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup on exit
        asyncio.run(cleanup())


if __name__ == "__main__":
    main()
