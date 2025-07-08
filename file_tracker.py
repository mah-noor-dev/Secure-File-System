# file_tracker.py
import os
import json
from datetime import datetime

class FileTracker:
    def __init__(self):
        self.index_file = os.path.join('metadata', 'file_index.json')
        os.makedirs('metadata', exist_ok=True)
        
        # Initialize with empty list if file doesn't exist or is empty
        if not os.path.exists(self.index_file) or os.path.getsize(self.index_file) == 0:
            with open(self.index_file, 'w') as f:
                json.dump([], f)
    
    def add_file_entry(self, original_name, encrypted_path, key_path):
        with open(self.index_file, 'r+') as f:
            try:
                files = json.load(f)
            except json.JSONDecodeError:
                files = []
                
            files.append({
                'original_name': original_name,
                'encrypted_path': encrypted_path,
                'key_path': key_path,
                'encryption_date': datetime.now().isoformat()
            })
            
            f.seek(0)
            json.dump(files, f, indent=2)
            f.truncate()
    
    def get_all_files(self):
        with open(self.index_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []