# SQL-for-Dummies:SQL Query Generator with LLM

## Overview
This project leverages a Large Language Model (LLM) to dynamically generate SQL queries based on natural language input. Users can create, modify, and query databases without needing to know SQL syntax. The application supports multiple tables and handles common variations in user input, making it user-friendly and efficient for database management.

## Features
- Create and delete tables dynamically.
- Insert, update, and delete records in the database.
- Execute complex SQL queries based on user input.
- Flexible interpretation of user commands to accommodate variations in terminology.

## Tech Stack
- **Backend**: Python
- **Database**: SQLite
- **LLM API**: Google Generative AI (e.g., Gemini, Bison)
- **Web Framework**: Streamlit for the user interface
- **Environment Management**: dotenv for environment variable management

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   pip install -r requirements.txt
   ```
Set up your environment variables in a .env file:
GOOGLE_API_KEY=<your-google-api-key>

Run the Streamlit app:
```
streamlit run sql.py
```
