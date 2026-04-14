import hashlib
import os

class Metadata:
    @staticmethod
    def get_file_hash(path):
        try:
            sha256_hash = hashlib.sha256()
            with open(path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (PermissionError, OSError):
            return None

    @staticmethod
    def scan_storage(base_dir):
        tree = {}
        if not os.path.exists(base_dir):
            return tree
            
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                file_hash = Metadata.get_file_hash(full_path)
                
                if file_hash:
                    tree[rel_path] = file_hash
        return tree