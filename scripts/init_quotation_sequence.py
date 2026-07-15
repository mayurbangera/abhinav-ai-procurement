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
        print("Creating sequence 'quotation_number_seq' if not exists...")
        db.execute(text("CREATE SEQUENCE IF NOT EXISTS quotation_number_seq START 1;"))
        
        # 2. Find the highest existing quotation number safely ignoring bad formats
        # Expected format: QT-YYYY-XXXX (e.g. QT-2026-0001)
        # We extract the last 4 digits.
        print("Calculating highest existing QT number...")
        query = text("""
            SELECT MAX(CAST(SUBSTRING(quotation_number FROM 9) AS INTEGER))
            FROM quotations 
            WHERE quotation_number ~ '^QT-[0-9]{4}-[0-9]{4}$'
        """)
        
        max_val = db.execute(query).scalar()
        
        if max_val:
            print(f"Highest existing quotation code is ...-{max_val:04d}")
            next_val = max_val + 1
            print(f"Setting sequence to start next at: {next_val}")
            
            # 3. Set the sequence value
            set_query = text(f"SELECT setval('quotation_number_seq', {next_val}, false);")
            db.execute(set_query)
        else:
            print("No existing valid QT codes found. Sequence will start at 1.")
            
        db.commit()
        print("Quotation sequence initialization completed successfully.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during sequence initialization: {str(e)}")
        # If the table doesn't exist yet, it will fail. That's fine if we run create_tables first.
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_sequence()
