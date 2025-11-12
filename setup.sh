#!/bin/bash

# Define the name of the virtual environment directory
VENV_NAME=".venv_tm"

echo "Creating virtual environment '$VENV_NAME'..."
python3 -m venv $VENV_NAME

echo "Activating virtual environment..."
source $VENV_NAME/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Ensure ipywidgets is correctly enabled for Jupyter Notebooks
echo "Enabling ipywidgets extension for Jupyter..."
jupyter nbextension enable --py widgetsnbextension

echo ""
echo "Setup complete!"
echo "To start working in the environment, run: source $VENV_NAME/bin/activate"
echo "You can now run Jupyter and test the 'turing_machine_app.py' script."