import sqlite3
from pathlib import Path

class WP3DatabaseGenerator:
    def __init__(self, database_file, overwrite=False):
        self.database_file = Path(database_file)
        self.database_overwrite = overwrite
        self.test_file_location()
        self.conn = sqlite3.connect(self.database_file)

    def generate_database(self):
        self.create_table_students()
        self.create_table_statements()
        self.create_table_teachers()

    def create_table_students(self):
        create_student = """
        CREATE TABLE IF NOT EXISTS studenten (
            studentnummer INTEGER PRIMARY KEY,
            Naam TEXT,
            Klas TEXT,
            ingevuld DATETIME,
            action_type TEXT,
            last_completed_statement INTERGER,
            Team TEXT,
            del DEFAULT 0);
        """
        self.__execute_transaction_statement(create_student)
        print("✅ Students table created")

    def create_table_statements(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS statement (
            id INTEGER PRIMARY KEY,
            choice_number TEXT,
            choice_text TEXT,
            choice_result VARCHAR(1)); 
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Statement table created")

    def create_table_teachers(self):
        create_teacher = """
        CREATE TABLE IF NOT EXISTS teachers (
            ID INTEGER PRIMARY KEY,
            Naam TEXT,
            Email TEXT,
            Wachtwoord TEXT,
            Actief_sinds DATETIME DEFAULT CURRENT_TIMESTAMP,
            Is_admin BOOLEAN DEFAULT 0,
            del DEFAULT 0);
        """
        self.__execute_transaction_statement(create_teacher)
        print("✅ Teachers table created")

    def __execute_transaction_statement(self, create_table_query):
        c = self.conn.cursor()
        c.execute(create_table_query)
        self.conn.commit()

    def test_file_location(self):
        if not self.database_file.parent.exists():
            raise ValueError(
                f"Database file location {self.database_file.parent} does not exist"
            )
        if self.database_file.exists():
            if not self.database_overwrite:
                raise ValueError(
                    f"Database file {self.database_file} already exists, set overwrite=True to overwrite"
                )
            else:
                self.database_file.unlink()
                print("✅ Database already exists, deleted")
        if not self.database_file.exists():
            try:
                self.database_file.touch()
                print("✅ New database setup")
            except Exception as e:
                raise ValueError(
                    f"Could not create database file {self.database_file} due to error {e}"
                )

if __name__ == "__main__":
    my_path = Path(__file__).parent.resolve()
    project_root = my_path.parent.parent
    database_path = project_root / "database" / "database.db"
    database_generator = WP3DatabaseGenerator(
        database_path, overwrite=True
    )
    database_generator.generate_database()
