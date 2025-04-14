#!/bin/bash

# Install pyenv and Python 3.7.0 (if not already installed)
echo "Installing pyenv and Python 3.7.0..."
curl https://pyenv.run | bash

# Add pyenv to your shell profile (for bash)
# echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
# echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
# echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# source ~/.bashrc

# Add pyenv to your shell profile (for zsh)
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# Install Python 3.7.0
pyenv install 3.7.0

# Set Python 3.7.0 as the global version (optional)
pyenv global 3.7.0

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3.7 -m venv .venv
source .venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Download the language model for spacy
python3 -m spacy download en_core_web_sm

# Instructions to deactivate
echo "Virtual environment is set up and activated. Use 'deactivate' to exit."