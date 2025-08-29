import os
import time
import hashlib
from pathlib import Path
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class DataMonitor:
    """Monitors CSV files for changes and triggers data updates"""
    
    def __init__(self):
        self.data_folder = Path(settings.BASE_DIR.parent) / 'Data'
        self.cache_key = 'csv_file_hashes'
        self.last_check = None
        
    def get_file_hash(self, file_path):
        """Get MD5 hash of a file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def get_all_csv_hashes(self):
        """Get hashes of all CSV files in Data folder"""
        hashes = {}
        if self.data_folder.exists():
            for csv_file in self.data_folder.glob('*.csv'):
                file_hash = self.get_file_hash(csv_file)
                if file_hash:
                    hashes[str(csv_file)] = {
                        'hash': file_hash,
                        'modified': csv_file.stat().st_mtime,
                        'size': csv_file.stat().st_size
                    }
        return hashes
    
    def check_for_changes(self):
        """Check if any CSV files have changed"""
        current_hashes = self.get_all_csv_hashes()
        cached_hashes = cache.get(self.cache_key, {})
        
        changes_detected = []
        
        for file_path, current_info in current_hashes.items():
            if file_path in cached_hashes:
                cached_info = cached_hashes[file_path]
                if (current_info['hash'] != cached_info['hash'] or 
                    current_info['modified'] != cached_info['modified'] or
                    current_info['size'] != cached_info['size']):
                    changes_detected.append(file_path)
                    logger.info(f"Change detected in {file_path}")
            else:
                # New file detected
                changes_detected.append(file_path)
                logger.info(f"New file detected: {file_path}")
        
        # Check for deleted files
        for file_path in cached_hashes:
            if file_path not in current_hashes:
                changes_detected.append(file_path)
                logger.info(f"File deleted: {file_path}")
        
        # Update cache with current hashes
        cache.set(self.cache_key, current_hashes, timeout=3600)  # Cache for 1 hour
        
        return changes_detected, current_hashes
    
    def get_last_modified_time(self):
        """Get the most recent modification time of any CSV file"""
        hashes = self.get_all_csv_hashes()
        if not hashes:
            return None
        
        latest_time = max(info['modified'] for info in hashes.values())
        return timezone.datetime.fromtimestamp(latest_time, tz=timezone.utc)
    
    def get_data_status(self):
        """Get current data status for frontend display"""
        hashes = self.get_all_csv_hashes()
        last_modified = self.get_last_modified_time()
        
        return {
            'total_files': len(hashes),
            'last_modified': last_modified.isoformat() if last_modified else None,
            'files': [
                {
                    'name': Path(file_path).name,
                    'size': info['size'],
                    'modified': timezone.datetime.fromtimestamp(info['modified'], tz=timezone.utc).isoformat()
                }
                for file_path, info in hashes.items()
            ]
        }

# Global instance
data_monitor = DataMonitor()
