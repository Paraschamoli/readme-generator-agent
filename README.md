<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">README Generator Agent</h1>
<h3 align="center">AI-Powered Documentation Automation</h3>

<p align="center">
  <strong>Automatic professional README generation from GitHub repositories with badge integration</strong><br/>
  Analyzes codebases and creates comprehensive documentation with installation guides, usage examples, and contribution guidelines
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/readme-generator-agent/actions/workflows/build-and-push.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/readme-generator-agent/build-and-push.yml?branch=main" alt="Build Status">
  </a>
  <a href="https://pypi.org/project/readme-generator-agent/">
    <img src="https://img.shields.io/pypi/v/readme-generator-agent" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version">
  <a href="https://github.com/Paraschamoli/readme-generator-agent/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Paraschamoli/readme-generator-agent" alt="License">
  </a>
</p>

---

## 🎯 What is README Generator Agent?

An AI-powered documentation assistant that automatically creates clear, structured, and professional README files for software projects. Think of it as having a technical writer who analyzes your code and creates perfect documentation automatically.

### Key Features
*   **🔍 Repository Analysis** - Deep analysis of GitHub repositories and codebases
*   **📄 Professional READMEs** - Comprehensive documentation with proper structure
*   **🛡️ Badge Integration** - Automatic badge generation (license, size, version, stars)
*   **📝 Clear Instructions** - Step-by-step installation and usage guides
*   **🔗 GitHub Integration** - Direct repository access and analysis
*   **⚡ Lazy Initialization** - Fast boot times, initializes on first request
*   **🔐 Secure API Handling** - No API keys required at startup

---

## 🛠️ Tools & Capabilities

### Built-in Tools
*   **GithubTools** - Repository analysis and metadata extraction
*   **LocalFileSystemTools** - README file creation and management
*   **Mem0Tools** - Memory and context retention (optional)

### README Generation Protocol
1.  **Repository Analysis** - Extract owner/repo_name from URL, analyze repository
2.  **Content Generation** - Create comprehensive README with professional structure
3.  **Formatting Standards** - Proper Markdown formatting with badges and code blocks
4.  **Quality Assurance** - Verify accuracy, check links, ensure professional tone

### Specific Requirements
- ❌ **DO NOT** include the project's languages-used section in the README
- ✅ **DO** include badges for license, repository size, version, etc.
- ✅ **DO** write the produced README to the local filesystem
- ✅ **DO** provide clear cloning and installation instructions

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. It takes 2 minutes and unlocks the full potential of your agent.

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/readme-generator-agent.git
cd readme-generator-agent

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key (choose one):
# OPENAI_API_KEY=sk-...              # For OpenAI GPT-4o
# OPENROUTER_API_KEY=sk-...          # For OpenRouter (cheaper alternative)
# GITHUB_ACCESS_TOKEN=ghp_...        # GitHub personal access token (required)
# MEM0_API_KEY=sk-...                # For memory features (optional)
```

### 3. Run Locally

```bash
# Start the README generator agent
python -m readme_generator_agent

# Or using uv
uv run python -m readme_generator_agent
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3773
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```env
# Choose ONE provider (both can be set, OpenAI takes priority)
OPENAI_API_KEY=sk-...              # OpenAI API key
OPENROUTER_API_KEY=sk-...          # OpenRouter API key (alternative)

# Required for GitHub repository access
GITHUB_ACCESS_TOKEN=ghp_...        # GitHub personal access token

# Optional - for enhanced features
MEM0_API_KEY=sk-...                # Mem0 API key for memory operations

# Optional
DEBUG=true                        # Enable debug logging
MODEL_NAME=openai/gpt-4o          # Model override
```

### GitHub Token Setup
1. Go to: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Generate new token with `repo` scope (full control of private repositories)
3. For public repos only, you can use token with `public_repo` scope

### Port Configuration
*   Default port: `3773` (can be changed in `agent_config.json`)

---

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a professional README for https://github.com/agno-agi/agno. Include badges, installation instructions, usage examples, and contribution guidelines. Do not include languages-used section."
      }
    ]
  }'
```

### Sample README Generation Queries

*   "Create documentation for my React project at github.com/username/react-app. Include TypeScript setup, environment variables, and deployment instructions."
*   "Write a professional README for a Python data science package. Include: installation with pip/conda, API documentation, examples with Jupyter notebooks, and citation information."
*   "Generate comprehensive documentation for a Node.js API project. Focus on: environment setup, API endpoints with examples, testing instructions, and Docker deployment."
*   "Create a README for a Go CLI tool. Include: cross-compilation instructions, command-line usage examples, configuration file format, and contribution workflow."
*   "Generate documentation for a machine learning repository. Include: dataset preparation, model training instructions, evaluation metrics, and inference examples."

### Expected Output Format

```markdown
# [Project Name]

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![GitHub repo size](https://img.shields.io/github/repo-size/{owner}/{repo})
![GitHub stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social)

## Description
Clear, comprehensive project description explaining what it does, why it exists, and who it's for...

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation
# Clone the repository
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# Install dependencies
{appropriate installation commands based on project type}

## Usage
{Example code showing basic usage}

## Features
* Feature 1: Detailed description with benefits
* Feature 2: Technical specifications and use cases
* Feature 3: Performance characteristics and limitations

## Configuration
{Environment variables, configuration files, or settings with examples}

## API Documentation
// Example API call
{api_client}.method({parameters})

## Contributing
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## License
This project is licensed under the {License Name} License - see the LICENSE file for details.

## Contact
Project Link: https://github.com/{owner}/{repo}
```

---

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t readme-generator-agent .

# Run container
docker run -d \
  -p 3773:3773 \
  -e OPENAI_API_KEY=your_key_here \
  -e GITHUB_ACCESS_TOKEN=your_github_token_here \
  --name readme-generator-agent \
  readme-generator-agent

# Check logs
docker logs -f readme-generator-agent
```

### Docker Compose (Recommended)

`docker-compose.yml`:
```yaml
version: '3.8'
services:
  readme-generator-agent:
    build: .
    ports:
      - "3773:3773"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GITHUB_ACCESS_TOKEN=${GITHUB_ACCESS_TOKEN}
      - MEM0_API_KEY=${MEM0_API_KEY}
    restart: unless-stopped
```

Run with Compose:
```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
readme-generator-agent/
├── readme_generator_agent/
│   ├── __init__.py          # Package initialization
│   ├── __version__.py       # Version information
│   └── main.py              # Main agent implementation
├── skills/
│   └── readme-generator/
│       └── skill.yaml       # Skill configuration
├── agent_config.json        # Bindu agent configuration
├── pyproject.toml           # Python dependencies
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Docker Compose setup
├── README.md                # This documentation
├── .env.example             # Environment template
└── uv.lock                  # Dependency lock file
```

---

## 🔌 API Reference

### Health Check
```bash
GET http://localhost:3773/health
```
Response:
```json
{"status": "healthy", "agent": "README Generator Agent"}
```

### Chat Endpoint
```bash
POST http://localhost:3773/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your README generation query here"}
  ]
}
```

### Agent Information
```bash
GET http://localhost:3773/agent/info
```

---

## 🧪 Testing

### Local Testing
```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with specific API keys
OPENAI_API_KEY=test_key GITHUB_ACCESS_TOKEN=test_token python -m pytest
```

### Integration Test
```bash
# Start agent
python -m readme_generator_agent &

# Test API endpoint
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Generate README for github.com/example/repo"}]}'
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

**"ModuleNotFoundError"**
```bash
uv sync --force
```

**"Port 3773 already in use"**
Change port in `agent_config.json` or kill the process:
```bash
lsof -ti:3773 | xargs kill -9
```

**"No API key provided"**
Check if `.env` exists and variable names match. Or set directly:
```bash
export OPENAI_API_KEY=your_key
export GITHUB_ACCESS_TOKEN=your_token
```

**"GitHub token required"**
Get a personal access token from GitHub settings:
```bash
# Generate token at: https://github.com/settings/tokens
# Required scopes: "repo" for private repos, "public_repo" for public only
```

**"Repository not found"**
Check repository URL format and ensure token has proper permissions.

**Docker build fails**
```bash
docker system prune -a
docker-compose build --no-cache
```

---

## 📊 Dependencies

### Core Packages
*   **bindu** - Agent deployment framework
*   **agno** - AI agent framework
*   **openai** - OpenAI client
*   **pygithub** - GitHub API integration
*   **python-dotenv** - Environment management
*   **mem0ai** - Memory operations (optional)
*   **requests** - HTTP requests
*   **rich** - Console output

### Development Packages
*   **pytest** - Testing framework
*   **ruff** - Code formatting/linting
*   **pre-commit** - Git hooks

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository
2.  Create a feature branch: `git checkout -b feature/improvement`
3.  Make your changes following the code style
4.  Add tests for new functionality
5.  Commit with descriptive messages
6.  Push to your fork
7.  Open a Pull Request

**Code Style:**
*   Follow PEP 8 conventions
*   Use type hints where possible
*   Add docstrings for public functions
*   Keep functions focused and small

---

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Acknowledgments
*   **Developer:** Paras Chamoli
*   **Framework:** Bindu - Agent deployment platform
*   **Agent Framework:** Agno - AI agent toolkit
*   **GitHub Integration:** PyGithub library
*   **Documentation Standards:** Open Source Initiative guidelines

---

## 🔗 Useful Links
*   🌐 **Bindu Directory:** [bindus.directory](https://bindus.directory)
*   📚 **Bindu Docs:** [docs.getbindu.com](https://docs.getbindu.com)
*   🐙 **GitHub:** [github.com/Paraschamoli/readme-generator-agent](https://github.com/Paraschamoli/readme-generator-agent)
*   💬 **Discord:** Bindu Community

<br/>

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Automating documentation to help developers focus on what matters most: building great software</em>
</p>
<p align="center">
  <a href="https://github.com/Paraschamoli/readme-generator-agent/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/Paraschamoli/readme-generator-agent/issues">🐛 Report Issues</a>
</p>

> **Note:** This agent follows the Bindu pattern with lazy initialization and secure API key handling. It boots without API keys and only fails at runtime if keys are needed but not provided.
