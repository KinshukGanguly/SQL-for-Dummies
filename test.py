import sqlite3
print(sqlite3.version)
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


models = genai.list_models()
for model in models:
    print(model)