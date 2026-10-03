import sqlite3

create_table = '<create_table_statement>'
sql_statements = [
    """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);"""
]



#To be fixed
def create_user(db: str, data: tuple[str, str]) -> bool:
    sql = ''' INSERT INTO users(username, password)
              VALUES(?,?) '''
    try:
        # The 'with' context manager automatically commits if successful
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, data)
            # conn.commit() is handled automatically by the context manager on success
            
            print("User created successfully")
            return True

    except sqlite3.OperationalError as e:
        print("Failed to open or write to database:", e)
        return False





def create_db(name: str):
    try:
        with sqlite3.connect(name) as conn:
            #functions should be here
            cursor = conn.cursor()
    
            for statement in sql_statements:
                cursor.execute(statement)
    
            conn.commit()
    
            print("Opened SQLite database successfully.")
    
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

