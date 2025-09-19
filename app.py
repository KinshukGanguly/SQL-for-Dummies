from dotenv import load_dotenv
load_dotenv()  
import streamlit as st
import os
import pandas as pd
import sqlite3
import google.generativeai as genai
import re


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#-------------------GETTING RESPONSE FROM GEMINI-------------------#
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([prompt[0], question])

    # Ensure text extraction works
    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text.strip()
    else:
        return ""

#-------------------EXECUTING SQL COMMAND-------------------#
def execute_sql_command(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        if sql.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            return rows
        else:
            conn.commit()
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

#-------------------EXTRACTING SQL FROM GEMINI RESPONSE-------------------#
def extract_sql(text: str) -> str:
    """
    Extract the first valid SQL command from Gemini response text.
    Looks for CREATE, SELECT, INSERT, UPDATE, DELETE, or DROP.
    """
    match = re.search(
        r"(CREATE|SELECT|INSERT|UPDATE|DELETE|DROP)[\s\S]+?;", 
        text, 
        re.IGNORECASE
    )
    return match.group(0).strip() if match else text.strip()

#-------------------PROMPT-------------------#
prompt = [
    """
You are an expert at converting natural language questions into precise and optimized SQL queries. Your role is to carefully interpret user input and produce the most relevant SQL command.

### Database Schema:
1. students
   - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - name (TEXT, NOT NULL)
   - age (INTEGER)
   - class_id (INTEGER, FOREIGN KEY → classes.id)
   - grade (TEXT)

2. teachers
   - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - name (TEXT, NOT NULL)
   - subject (TEXT)
   - class_id (INTEGER, FOREIGN KEY → classes.id)

3. classes
   - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
   - name (TEXT, NOT NULL)
   - section (TEXT)

### Guidelines for Query Generation:
- Always use the above schema (students, teachers, classes).
- Database name is not required in queries.
- Interpret synonyms, abbreviations, and variations in phrasing. Examples:
  - "roll" → id
  - "grade" → grade
  - "how many students?" → SELECT COUNT(*) FROM students;
- Ensure SQL syntax is correct, efficient, and follows best practices.
- Do not include extra text like "SQL" or triple backticks.

### Example Conversions:

1. Table Creation
   - Input: "Create a table TEACHER with columns NAME and SUBJECT."
     Output: CREATE TABLE teachers (name TEXT, subject TEXT);

   - Input: "Create a STUDENT table with NAME, CLASS, SECTION, and AGE."
     Output: CREATE TABLE students (name TEXT, age INT, class_id INT, grade TEXT);

2. Data Insertion
   - Input: "Add a new student named John in Mathematics section A."
     Output: INSERT INTO students (name, age, class_id, grade) VALUES ('John', 15, 1, 'A');

   - Input: "Insert a teacher Jane who teaches Mathematics."
     Output: INSERT INTO teachers (name, subject, class_id) VALUES ('Jane', 'Mathematics', 1);

3. Data Retrieval
   - Input: "Show all students in section A."
     Output: SELECT s.* FROM students s JOIN classes c ON s.class_id = c.id WHERE c.section = 'A';

   - Input: "Get the total number of students."
     Output: SELECT COUNT(*) FROM students;

4. Update Requests
   - Input: "Update John's grade to B."
     Output: UPDATE students SET grade = 'B' WHERE name = 'John';

   - Input: "Change the subject of Jane to Physics."
     Output: UPDATE teachers SET subject = 'Physics' WHERE name = 'Jane';

5. Deletion Requests
   - Input: "Remove the student named John."
     Output: DELETE FROM students WHERE name = 'John';

   - Input: "Drop the teachers table."
     Output: DROP TABLE IF EXISTS teachers;

6. Advanced Queries
   - Input: "List all students in Mathematics class."
     Output: SELECT s.* FROM students s JOIN classes c ON s.class_id = c.id WHERE c.name = 'Mathematics';

   - Input: "Find the average age of students in Science class."
     Output: SELECT AVG(s.age) FROM students s JOIN classes c ON s.class_id = c.id WHERE c.name = 'Science';

### Additional Considerations:
- Handle plural vs. singular (students vs. student).
- Resolve ambiguities reasonably when columns are not explicitly named.
- Do not assume data unless mentioned.
- Avoid SQL injection by sanitizing inputs.
- Output only the SQL query, nothing else.
"""
]


st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("A Dummy's Guide to SQL")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    print("Raw Gemini response:", response)

    sql_query = extract_sql(response)
    print("Extracted SQL:", sql_query)

    result = execute_sql_command(sql_query, "school.db")
    print(result)
    
    if result is not None:
        st.subheader("Query Results:")
        for row in result:
            st.write(row)   # clean output in app
    else:
        st.success("✅ Command executed successfully (no results to display).")
