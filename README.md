## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install google-adk
adk create my_agent
echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > .env
```

## Config other models

```sh
# Please see below guide to configure other models:
https://google.github.io/adk-docs/agents/models
```

## Run

```sh
# Run with command-line interface
adk run my_agent

# Run with web interface
adk web --port 8000
```