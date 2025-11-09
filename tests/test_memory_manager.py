import os
import json
import shutil
import pytest
from core.memory_manager import MemoryManager

TEST_MEMORY_DIR = "data/test_memory"


@pytest.fixture(autouse=True)
def clean_test_environment():
    """Cleans up the test directory before and after tests."""
    if os.path.exists(TEST_MEMORY_DIR):
        shutil.rmtree(TEST_MEMORY_DIR)
    os.makedirs(TEST_MEMORY_DIR, exist_ok=True)
    yield
    shutil.rmtree(TEST_MEMORY_DIR)


def test_initialization_creates_files():
    """Tests if the MemoryManager initializes and creates the directory/files."""
    mm = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    assert isinstance(mm.memory_data, dict)
    assert isinstance(mm.context_data, (dict, list))
    assert os.path.isdir(TEST_MEMORY_DIR)


def test_set_and_get_memory_data(): # Updated Test Name
    """Tests saving and loading a memory entry using new method names."""
    mm = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    # FIX: Use new method name
    mm.set_memory_entry("favorite_color", {"score": 1, "text": "I like blue"}) 
    
    mm2 = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    # FIX: Use new method name
    loaded = mm2.get_memory_data("favorite_color") 
    assert loaded["score"] == 1


def test_clear_memory():
    """Tests clearing the memory data."""
    mm = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    # FIX: Use new method name
    mm.set_memory_entry("nickname", {"score": 2}) 
    mm.clear_memory()
    # FIX: Use new method name
    assert mm.get_memory_data() == {} 
    with open(mm.memory_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == {}

        
def test_get_memory_metadata(): # New Test
    """Tests the new get_memory_metadata method."""
    mm = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    mm.set_memory_entry("book", {"score": 0.5})
    mm.set_memory_entry("movie", {"score": 0.9})
    
    metadata = mm.get_memory_metadata()
    assert metadata["total_entries"] == 2
    assert "last_updated" in metadata


def test_save_and_load_context():
    """Tests saving and loading the conversation context."""
    mm = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    mm.save_context(messages)

    mm2 = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    loaded = mm2.load_context()
    assert loaded == messages


def test_clear_context():
    """Tests clearing the conversation context."""
    mm = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    mm.save_context([{"role": "user", "content": "Hi"}])
    mm.clear_context()
    assert mm.load_context() == []


def test_load_json_handles_corruption_gracefully():
    """Tests robustness when memory files are corrupt."""
    mm = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    # Corrupt memory file
    with open(mm.memory_file, "w", encoding="utf-8") as f:
        f.write("{not valid json}")
    mm2 = MemoryManager(memory_dir=TEST_MEMORY_DIR)
    assert mm2.memory_data == {}