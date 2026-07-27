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

## Install Google CLI

```sh
# Update package lists and install core prerequisites:
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates gnupg curl

# Import the Google Cloud public encryption key:
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

# Register the signed distribution repository list:
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

# Refresh the system package database index and install:
sudo apt-get update && sudo apt-get install -y google-cloud-cli

# Verify everything functions perfectly:
gcloud --version


# Step 2: Initialize and Authenticate Your Environment
# Once installed, you must link the CLI tool to your live Google Cloud account.

# Trigger the initialization sequence:
gcloud init

# Step 3: Run Your Build Command
# Now that gcloud is active, swap out YOUR_PROJECT_ID with your actual, unique Google Cloud Project ID and execute your container submission:
# gcloud builds submit --tag gcr.io/your-actual-project-id/adk-agent:latest
gcloud builds submit --tag gcr.io/agent-deployment-245/adk-agent:latest --project=agent-deployment-245

# Deploy the container image into production:
gcloud run deploy adk-agent \
  --image gcr.io/agent-deployment-245/adk-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
  


export GOOGLE_CLOUD_PROJECT=agent-deployment-245
export GOOGLE_CLOUD_LOCATION=us-central1 # Or your preferred location
export GOOGLE_GENAI_USE_ENTERPRISE=True

# The deployed service exposes a small HTTP API and Swagger UI at /docs.
# For the ADK local web UI, run `adk web` on your machine instead of Cloud Run.
```


## Submit to production: google cloud

```sh
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/adk-agent:latest

## 
curl -X POST https://adk-agent-ztqxnnjk4q-uc.a.run.app/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"What time is it in London?","user_id":"demo-user"}'
```