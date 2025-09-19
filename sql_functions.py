import os
import sqlite3

def create_database(db_name):
    """Create a SQLite database with given name if not exists."""
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        conn.close()
        print(f"Database '{db_name}' created successfully.")
    else:
        print(f"Database '{db_name}' already exists.")

def create_tables(db_name):
    """Create sample school tables: students, teachers, classes."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            class_id INTEGER,
            grade TEXT,
            FOREIGN KEY(class_id) REFERENCES classes(id)
        );
    ''')

    # Teachers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT,
            class_id INTEGER,
            FOREIGN KEY(class_id) REFERENCES classes(id)
        );
    ''')

    # Classes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            section TEXT
        );
    ''')

    conn.commit()
    conn.close()
    print("Tables created successfully.")

def insert_sample_data(db_name):
    """Insert some sample rows into the school tables."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert classes
    cursor.executemany("INSERT INTO classes (name, section) VALUES (?, ?)", [
        ("Mathematics", "A"),
        ("Science", "B"),
        ("History", "A"),
    ])

    # Insert students
    cursor.executemany("INSERT INTO students (name, age, class_id, grade) VALUES (?, ?, ?, ?)", [
        ("Alice", 14, 1, "A"),
        ("Bob", 15, 2, "B"),
        ("Charlie", 13, 3, "A"),
    ])

    # Insert teachers
    cursor.executemany("INSERT INTO teachers (name, subject, class_id) VALUES (?, ?, ?)", [
        ("Mr. Smith", "Mathematics", 1),
        ("Ms. Johnson", "Science", 2),
        ("Mr. Lee", "History", 3),
    ])

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")


if __name__ == "__main__":
    db_name = "school.db"   
    create_database(db_name)
    create_tables(db_name)
    insert_sample_data(db_name)
