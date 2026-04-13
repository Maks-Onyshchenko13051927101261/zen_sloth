import os
from fastapi import HTTPException

class Security:
    @staticmethod
    def get_safe_path(base_dir: str, filename: str) -> str:
        """Запобігає Path Traversal атакам."""
        target_path = os.path.abspath(os.path.join(base_dir, filename))
        if not target_path.startswith(os.path.abspath(base_dir)):
            raise HTTPException(
                status_code=403, 
                detail="Access denied: attempt to exit sandbox"
            )
        return target_path