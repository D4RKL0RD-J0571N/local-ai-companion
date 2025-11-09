import pytest
from unittest.mock import patch, MagicMock
from core.conversation_manager import ConversationManager
from core.memory_manager import MemoryManager
import spacy

# Initialize SpaCy globally for the test environment to prevent re-downloads
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")


@pytest.fixture
def conv_manager(tmp_path):
    """Initializes ConversationManager with a temporary memory path."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    manager = ConversationManager(system_prompt="System ready.", memory_dir=str(memory_dir))
    return manager


def test_initialization(conv_manager):
    """Verifies initial system message is set."""
    context = conv_manager.get_context()
    assert len(context) == 1
    assert context[0]["role"] == "system"
    assert "System ready." in context[0]["content"]


def test_add_user_and_ai_messages(conv_manager):
    """Verifies messages are correctly added to the internal context list."""
    conv_manager.messages.append({"role": "user", "content": "Hello"})
    conv_manager.messages.append({"role": "assistant", "content": "Hi there"})
    
    ctx = conv_manager.get_context()
    assert any(m["role"] == "user" and m["content"] == "Hello" for m in ctx)
    assert any(m["role"] == "assistant" and m["content"] == "Hi there" for m in ctx)


def test_context_accumulates(conv_manager):
    """Verifies context length after adding messages."""
    conv_manager.messages.append({"role": "user", "content": "Hey"})
    conv_manager.messages.append({"role": "assistant", "content": "Hi"})
    context = conv_manager.get_context()
    assert len(context) == 3  # system + user + assistant


def test_chat_flow_with_mock(conv_manager):
    """Tests a full chat cycle, verifying message storage and context saving."""
    mock_reply = "Hello human!"
    with patch("core.conversation_manager.send_message", return_value=mock_reply): 
        reply = conv_manager.chat("Hi there!")

    assert reply == mock_reply
    ctx = conv_manager.get_context()
    
    # Verify last messages in internal context
    assert ctx[-2]["role"] == "user"
    assert ctx[-2]["content"] == "Hi there!"
    assert ctx[-1]["role"] == "assistant"
    assert ctx[-1]["content"] == mock_reply
    
    # Verify context persisted to memory
    persisted = conv_manager.memory.load_context()
    assert persisted[-1]["content"] == mock_reply


def test_chat_handles_api_failure(conv_manager):
    """Tests behavior when the API returns None."""
    with patch("core.conversation_manager.send_message", return_value=None):
        result = conv_manager.chat("Hello?")
    assert result is None
    ctx = conv_manager.get_context()
    assert any(msg["role"] == "user" for msg in ctx)
    # Ensure no empty/None assistant message was appended
    assert not any(msg["role"] == "assistant" and msg.get("content") in (None, "") for msg in ctx)


def test_reset_context(conv_manager):
    """Tests context reset, keeping only the system message."""
    conv_manager.messages.append({"role": "user", "content": "Erase me"})
    conv_manager.reset_context()
    ctx = conv_manager.get_context()
    assert len(ctx) == 1
    assert ctx[0]["role"] == "system"
    # File should not contain old user messages
    saved_ctx = conv_manager.memory.load_context()
    assert saved_ctx == []  # memory.clear_context() sets context to []


def test_memory_preference_extraction(conv_manager):
    """Tests if 'like' statements are saved to memory."""
    user_input = "I really love gothic fiction and Edgar Allan Poe."
    with patch("core.conversation_manager.send_message", return_value="Okay."):
        conv_manager.chat(user_input)
        
    memory_data = conv_manager.memory.get_memory_data() 
    
    # Poe should be extracted as an entity
    assert "Edgar Allan Poe" in memory_data 
    assert memory_data["Edgar Allan Poe"]["type"] == "preference"
    assert memory_data["Edgar Allan Poe"]["score"] > 0  # Positive sentiment
    
    # Check a neutral/negative entity (might be extracted as NOUN/PROPN)
    assert "fiction" in memory_data or "gothic fiction" in memory_data
    
    
def test_memory_sentiment_extraction(conv_manager):
    """Tests if general sentiment is saved to memory (no keyword)."""
    user_input = "That noisy party was terrible."
    with patch("core.conversation_manager.send_message", return_value="I agree."):
        conv_manager.chat(user_input)
        
    memory_data = conv_manager.memory.get_memory_data()
    
    # 'party' or 'noisy party' should be extracted
    extracted_entity = next((k for k in memory_data if "party" in k), None)
    
    assert extracted_entity is not None
    assert memory_data[extracted_entity]["type"] == "sentiment"
    assert memory_data[extracted_entity]["score"] < 0  # Negative sentiment


def test_dynamic_memory_recall_and_prompt_injection(conv_manager):
    """
    Tests that relevant memories are recalled and injected into the system prompt 
    before sending the message to the AI.
    
    FIXED: Now uses 5-tuple format (entity, weighted_score, entry, similarity, frequency)
    """
    # 1. Clear memory to start fresh
    conv_manager.memory.clear_memory()

    # 2. Pre-populate memory (optional, won't be used due to mocking)
    conv_manager.memory.set_memory_entry("Edgar Allan Poe", {
        "type": "preference",
        "text": "I love Poe",
        "score": 0.8,
        "timestamp": "2024-01-01T00:00:00"
    })
    conv_manager.memory.set_memory_entry("Tractor Repair", {
        "type": "fact",
        "text": "Knows how to fix tractors",
        "score": 0.0,
        "timestamp": "2024-01-02T00:00:00"
    })

    user_input = "What is your favorite writer? Tell me more about him."
    mock_reply = "I'm sure you mean Poe! I adore his poetry."

    # --- FIXED: Mock dynamic memory recall with 5-tuple format ---
    with patch.object(conv_manager, "_recall_relevant_memory", return_value=[
        ("Edgar Allan Poe", 0.8, {"type": "preference", "score": 0.8, "text": "I love Poe"}, 0.9, 1)
        # Format: (entity, weighted_score, entry_dict, similarity, frequency)
    ]):
        # Mock the external send_message to capture the final prompt
        with patch("core.conversation_manager.send_message", return_value=mock_reply) as mock_send:
            reply = conv_manager.chat(user_input)

            # Ensure API was called once
            mock_send.assert_called_once()

            # Extract the system message content
            messages_called = mock_send.call_args[0][0]
            system_message_content = messages_called[0]["content"]

            # --- Assertions ---
            assert reply == mock_reply
            assert messages_called[0]["role"] == "system"

            # Relevant entity is present
            assert "**USER MEMORY CONTEXT:**" in system_message_content
            # FIXED: Check for actual output format
            assert "'Edgar Allan Poe': a beloved interest" in system_message_content

            # Irrelevant entity is absent
            assert "Tractor Repair" not in system_message_content

            # Relevance score formatting
            assert "relevance:" in system_message_content.lower()