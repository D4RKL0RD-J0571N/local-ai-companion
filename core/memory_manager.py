import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self, memory_dir="data/memory", memory_file="memory.json", context_file="context.json"):
        self.memory_dir = memory_dir
        self.memory_file = os.path.join(memory_dir, memory_file)
        self.context_file = os.path.join(memory_dir, context_file)
        os.makedirs(memory_dir, exist_ok=True)
        self.memory_data = self._load_json(self.memory_file)
        self.context_data = self._load_json(self.context_file)

    # ----- Memory -----
    def set_memory_entry(self, key, value): # Refactored/Renamed
        """Sets a single key-value entry in memory_data."""
        self.memory_data[key] = value
        # Update timestamp for metadata
        self.memory_data["_last_updated"] = datetime.now().isoformat() 
        self._save_json(self.memory_file, self.memory_data)

    def get_memory_data(self, key=None): # Refactored/Renamed
        """Returns the full memory data or a specific key's value."""
        if key:
            return self.memory_data.get(key)
        return self.memory_data

    def clear_memory(self):
        self.memory_data = {}
        self._save_json(self.memory_file, self.memory_data)
        
    def get_memory_metadata(self): # New Method (Fixes summarize_all bug)
        """Returns metadata about the memory state."""
        return {
            # Count entries, excluding internal keys like _last_updated
            "total_entries": sum(1 for k in self.memory_data if not k.startswith("_")),
            "last_updated": self.memory_data.get("_last_updated", "never"),
        }

    # ----- Context -----
    def save_context(self, context):
        self.context_data = context
        self._save_json(self.context_file, self.context_data)

    def load_context(self):
        return self.context_data or []

    def clear_context(self):
        self.context_data = []
        self._save_json(self.context_file, self.context_data)

    # ----- JSON helpers -----
    def _load_json(self, path):
        if not os.path.exists(path):
            return {} if "memory" in path else []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {} if "memory" in path else []

    def _save_json(self, path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)