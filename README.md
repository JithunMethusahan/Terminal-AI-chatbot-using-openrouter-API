```markdown
# Terminal AI Chatbot using OpenRouter API

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A lightweight, terminal-based AI chatbot that leverages the OpenRouter API to provide intelligent conversational experiences directly in your terminal. Built for developers and enthusiasts who want a simple yet powerful AI assistant without heavy dependencies.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Features

-  **Lightweight & Fast**: No heavy GUI—just your terminal and the AI.
- 🔌 **OpenRouter Integration**: Access to multiple AI models through a single API.
- 🛠️ **Easy Configuration**: Simple setup with environment variables.
- 🧩 **Extensible**: Easy to modify and extend with new features.
- 🔒 **Secure**: No data stored—everything happens in your terminal.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JithunMethusahan/Terminal-AI-chatbot-using-openrouter-API.git
   cd Terminal-AI-chatbot-using-openrouter-API
   ```

2. **Install dependencies** (ensure you have Python 3.8+ installed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (get one from [OpenRouter](https://openrouter.com)):
   ```bash
   echo "export OPENROUTER_API_KEY='your-api-key-here'" >> ~/.bashrc
   source ~/.bashrc
   ```

## Usage

1. **Run the chatbot**:
   ```bash
   python main.py
   ```

2. **Interact with the chatbot**:
   - Type your message and press Enter.
   - The AI will respond in real-time.
   - Type `exit` or `quit` to end the session.

3. **Example**:
   ```
   You: Hello, how are you?
   AI: I'm just a program, but thanks for asking! How can I assist you today?
   ```

## Configuration

You can customize the behavior by setting environment variables:

- `OPENROUTER_API_KEY`: Your API key from OpenRouter.
- `MODEL_NAME`: The specific model to use (e.g., `gpt-3.5-turbo`).
- `TEMPERATURE`: Controls response randomness (0.0 to 1.0).

Example `.env` file (create one in the project root):
```ini
OPENROUTER_API_KEY=your_api_key_here
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Report bugs
- Suggest new features
- Submit pull requests

We are committed to providing a welcoming and inclusive environment for all contributors. Please adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

This README provides a professional structure with clear sections for easy navigation. It includes:

- A concise title and description
- Badges for license and PRs (using placeholders since actual URLs aren't provided)
- A table of contents for longer READMEs
- Clear installation and usage instructions
- Configuration details for advanced users
- A contributing section to encourage community involvement
- A standard MIT license notice

The template follows the "simple-complex" style by starting with a clean, minimal setup but including advanced sections for those who want to dive deeper.
