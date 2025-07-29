import os
import csv

#### Taken from probable microservice 1 code from teammate for purpose of Milestone #1 Demo

def handle_import():
    """Import CSV data from ./import.csv"""
    try:
        if not os.path.exists("./import.csv"):
            return {"status": "error", "message": "import.csv not found", "data": None}
        with open("./import.csv", 'r') as f:
            data = list(csv.DictReader(f))
            print(data)
        return {"status": "success", "message": f"Imported {len(data)} records", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": None}