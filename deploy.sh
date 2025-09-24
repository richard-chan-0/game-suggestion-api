#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the environment parameter is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <environment>"
  exit 1
fi

ENVIRONMENT=$1

# Run the commands
./copy_src_to_layer.sh
sam build
sam deploy --config-env "$ENVIRONMENT"

# Reminder to update environment variables after deployment
echo "Reminder: Update environment variables for your Lambda functions. AWS Lambda clears them on each deploy."