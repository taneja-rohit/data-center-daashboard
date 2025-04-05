import streamlit as st
import os
import sys

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app
from app.app import main

# Run the app
if __name__ == "__main__":
    main() 