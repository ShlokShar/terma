# Terma

A lightweight Python CLI tool that converts natural language instructions into terminal commands.

## Overview

**Terma** lets you describe what you want to do in plain English, and your configured AI provider (OpenAI, Anthropic, or Google GenAI) will translate it into a valid terminal command.

## Features

- Convert natural language directly into executable commands
- Multiple AI provider support:
  - **OpenAI**
  - **Anthropic**
  - **Google GenAI**
- AI agent configuration via `terma config`
- Persistent settings stored automatically at `~/.config/terma/config.json`
- Simple CLI tool created with **Python** + **Typer**

## Installation

### Globally

You can install Terma through PyPI:
```bash
pip install terma
```

### Locally
```bash
git clone https://github.com/ShlokShar/terma.git
cd terma
pip install -e .
```

## Usage

### Basic Syntax
```bash
terma <command> <args>
```

## Configuration

Terma uses a simple config system to set your AI provider, API key, and model. Configuration is **required** prior to executing the natural language command.

### Supported config commands

| Command | Description |
|---------|-------------|
| `terma config provider <provider>` | Set the AI provider (e.g., `openai`, `anthropic`, `google`) & API key |
| `terma config provider <provider> --api-key <key>` | Set provider and API key in one line |
| `terma config api-key` | Set the API key separately |
| `terma config model <model-name>` | Sets the model (e.g., `gpt-4-nano`, `claude-haiku-4-5`, etc.) |
| `terma config peek` | View Terma's current configuration |

## Natural Language Execution

Translate any natural language instruction into a real command:
```bash
terma exec <instruction>
```

## Example Commands

**Input:**
```bash
terma exec check node version
```

**Output:**
```bash
node --version
```

---

**Input:**
```bash
terma exec make a new directory called logs and move all .txt files into it
```

**Output:**
```bash
mkdir logs && mv *.txt logs/
```

*(Actual output may differ depending on the AI provider/model.)*

## Config File Path

Terma automatically stores configuration settings at:
```
~/.config/terma/config.json
```

You do not need to create this manually.

## License

This project is licensed under the **MIT License**.

## Contributing

Feel free to open issues, submit PRs, or propose features.

## Roadmap

- Command history log for past AI-generated commands
- More provider-specific settings
- Optional safety/output confirmation mode

## Author

**Shlok Sharma**  
GitHub: [@ShlokShar](https://github.com/ShlokShar)

## Related Projects

- **insectool** — A lightweight Python web scanner for identifying common web vulnerabilities