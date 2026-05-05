import mysql.connector

def setup_database():
    try:
        # Connect without specific database to create it if it doesn't exist
        print("Connecting to MySQL...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="votingsystem"
        )
        cursor = conn.cursor()
        
        # Create database
        print("Creating database 'voting_system'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS voting_system")
        cursor.execute("USE voting_system")
        
        # Create users table
        print("Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                face_encoding LONGBLOB NOT NULL,
                has_voted BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Create candidates table
        print("Creating 'candidates' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """)
        
        # Create votes table
        print("Creating 'votes' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                candidate_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (candidate_id) REFERENCES candidates(id)
            )
        """)

        # Insert some default candidates if the table is empty
        cursor.execute("SELECT COUNT(*) FROM candidates")
        if cursor.fetchone()[0] == 0:
            print("Populating default candidates...")
            cursor.execute("INSERT INTO candidates (name) VALUES ('Alice Smith')")
            cursor.execute("INSERT INTO candidates (name) VALUES ('Bob Jones')")
            cursor.execute("INSERT INTO candidates (name) VALUES ('Charlie Brown')")
            
        conn.commit()
        print("Database setup complete! All tables and initial data are ready.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    setup_database()
