#!/bin/bash

# LLM Cognitive Framework Deployment Script
# This script sets up and deploys the cognitive profiling framework

set -e  # Exit on error

echo "========================================="
echo "LLM Cognitive Framework Deployment"
echo "========================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$python_version" ]]; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
print_status "Python version: $python_version"

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
print_status "Downloading spaCy language model..."
python -m spacy download en_core_web_sm

# Check for .env file
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_warning "Please edit .env file and add your API keys!"
    echo ""
    echo "Required API keys:"
    echo "  - OPENAI_API_KEY"
    echo "  - ANTHROPIC_API_KEY"
    echo "  - GOOGLE_API_KEY"
    echo "  - DEEPSEEK_API_KEY"
    echo ""
    read -p "Press enter to open .env file in editor (or Ctrl+C to exit)..."
    ${EDITOR:-nano} .env
fi

# Create necessary directories
print_status "Creating directories..."
mkdir -p results visualizations logs config/task_templates

# Validate API keys
print_status "Validating configuration..."
python -c "
from src.utils.config import Config
config = Config('config/config.yaml')
models_with_keys = []
for model_name, model_config in config.get('models', {}).items():
    if model_config.get('api_key'):
        models_with_keys.append(model_name)
        print(f'  ✓ {model_name} API key configured')
    else:
        print(f'  ✗ {model_name} API key missing')
if not models_with_keys:
    print('\\nWarning: No API keys configured!')
else:
    print(f'\\nReady to test: {', '.join(models_with_keys)}')
"

echo ""
print_status "Setup complete!"
echo ""
echo "To run the framework:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run comparative assessment: python main.py --compare"
echo "  3. View results in: results/ and visualizations/"
echo ""
echo "For Docker deployment:"
echo "  docker-compose up --build"
echo ""
print_status "Happy profiling!"
