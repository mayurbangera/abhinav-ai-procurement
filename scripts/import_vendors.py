import csv
import re
from datetime import datetime
from sqlalchemy.orm import Session

import sys
import os

# Add parent directory to path to allow imports from 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import SessionLocal
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate

def extract_gst(gst_string: str) -> str:
    if not gst_string:
        return ""
    # Extract the 15 char GST number from a string like "Maharashtra-27BBBPB8888P903, ..."
    # Extract the 15 char GST number
    gst_pattern = r'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{3}'
    matches = re.findall(gst_pattern, gst_string.upper())
    if matches:
        return matches[0]
    return ""

def clean_mobile(mobile_str: str) -> str:
    if not mobile_str:
        return ""
    # Extract only digits
    digits = "".join(filter(str.isdigit, mobile_str))
    if len(digits) >= 10:
        return digits[-10:] # Take last 10 digits
    return ""

def import_legacy_vendors(csv_path: str):
    db: Session = SessionLocal()
    
    print(f"Reading {csv_path}...")
    
    # Store vendors in a dict by Supplier_Name to merge categories
    vendors_dict = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Skip the first line (title)
            next(f)
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                name = row.get('Supplier_Name', '')
                if name is None:
                    continue
                name = name.strip()
                if not name:
                    continue
                    
                category = row.get('Category_Name', '')
                if category is not None:
                    category = category.strip()
                else:
                    category = ""
                
                if name not in vendors_dict:
                    vendors_dict[name] = {
                        'row_data': row,
                        'categories': set()
                    }
                
                if category:
                    vendors_dict[name]['categories'].add(category)
                    
        print(f"Found {len(vendors_dict)} unique vendors to process.")
        
        success_count = 0
        error_count = 0
        
        for name, data in vendors_dict.items():
            row = data['row_data']
            categories = list(data['categories'])
            
            raw_gst = row.get('GSTRegNos', '')
            gst = extract_gst(raw_gst)
            
            if not gst:
                # If no valid GST, we cannot insert because gst_number is mandatory and unique
                print(f"Skipping {name}: No valid GST found in '{raw_gst}'")
                error_count += 1
                continue
                
            existing_supplier = db.query(Supplier).filter(Supplier.gst_number == gst).first()
            if existing_supplier:
                print(f"Skipping {name}: GST {gst} already exists.")
                error_count += 1
                continue
                
            mobile = clean_mobile(row.get('Mobile', ''))
            if not mobile:
                mobile = clean_mobile(row.get('Phone', ''))
            if not mobile:
                mobile = "0000000000" # Fallback if mobile is missing
                
            email = row.get('Email', '').strip()
            
            # We must provide dummy values for mandatory fields that aren't in the Excel
            address = row.get('Address', '').strip() or row.get('Address_Off', '').strip() or "No Address Provided"
            contact_person = row.get('Owner/Contact Person', '').strip() or "N/A"
            bank_name = "N/A"
            beneficiary_name = "N/A"
            bank_account = "00000000"
            bank_ifsc = "XXXX0000000"
            
            supplier_category = ", ".join(categories)
            
            # Generate VEND code
            last_vendor = db.query(Supplier).filter(Supplier.supplier_code.isnot(None)).order_by(Supplier.id.desc()).first()
            if last_vendor and last_vendor.supplier_code and last_vendor.supplier_code.startswith("VEND"):
                try:
                    last_num = int(last_vendor.supplier_code.replace("VEND", ""))
                    new_num = last_num + 1
                except ValueError:
                    new_num = 1
            else:
                new_num = 1
                
            supplier_code = f"VEND{new_num:06d}"
            
            new_supplier = Supplier(
                company_name=name,
                gst_number=gst,
                registered_address=address,
                contact_person_name=contact_person,
                contact_person_email=email if '@' in email else None,
                whatsapp_number=mobile,
                supplier_category=supplier_category,
                bank_name=bank_name,
                beneficiary_name=beneficiary_name,
                bank_account_number=bank_account,
                bank_ifsc=bank_ifsc,
                registration_status="APPROVED",
                supplier_code=supplier_code
            )
            
            try:
                db.add(new_supplier)
                db.commit()
                success_count += 1
            except Exception as e:
                db.rollback()
                print(f"Error inserting {name}: {e}")
                error_count += 1
                
        print(f"Import Complete: {success_count} successfully imported, {error_count} skipped/errors.")
        
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_vendors.py <path_to_csv>")
        sys.exit(1)
        
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        sys.exit(1)
        
    import_legacy_vendors(csv_file)
