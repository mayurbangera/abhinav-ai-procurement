import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.database.database import SessionLocal

def init_sequence():
    db = SessionLocal()
    try:
        # 1. Create the sequence if it doesn't exist
        print("Creating sequence 'supplier_code_seq' if not exists...")
        db.execute(text("CREATE SEQUENCE IF NOT EXISTS supplier_code_seq START 1;"))
        
        # 2. Find the highest existing supplier code safely ignoring bad formats
        print("Calculating highest existing VEND number...")
        # We look for codes matching VEND followed by exactly 6 digits to ignore bad data.
        query = text("""
            SELECT MAX(CAST(SUBSTRING(supplier_code FROM 5) AS INTEGER))
            FROM suppliers 
            WHERE supplier_code ~ '^VEND[0-9]{6}$'
        """)
        
        max_val = db.execute(query).scalar()
        
        if max_val:
            print(f"Highest existing supplier code is VEND{max_val:06d}")
            next_val = max_val + 1
            print(f"Setting sequence to start next at: {next_val}")
            
            # 3. Set the sequence value
            # is_called = false means the next nextval() will return this exact value.
            set_query = text(f"SELECT setval('supplier_code_seq', {next_val}, false);")
            db.execute(set_query)
        else:
            print("No existing valid VEND codes found. Sequence will start at 1.")
            
        db.commit()
        print("Sequence initialization completed successfully.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during sequence initialization: {str(e)}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_sequence()
