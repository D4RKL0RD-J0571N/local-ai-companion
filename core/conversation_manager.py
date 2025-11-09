from rich.table import Table
from core.memory_manager import MemoryManager
from core.api_connector import send_message 
from datetime import datetime
import spacy
from textblob import TextBlob
import logging
import warnings
import math
from collections import Counter

# Configure logging for better error visibility
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Initialize Spacy globally
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Downloading en_core_web_md model. This may take a moment.")
    import spacy.cli
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")


class ConversationManager:
    """Manages conversation flow and coordinates memory/context interaction with enhanced tracking."""

    def __init__(
        self, 
        system_prompt="", 
        memory_dir="data/memory", 
        entity_noun_limit=5, 
        similarity_threshold=0.6, 
        memory_recall_limit=5,
        max_context_messages=20
    ):
        self.memory = MemoryManager(memory_dir)
        self.system_prompt_base = system_prompt or "You are a helpful AI companion."
        self.messages = [
            {"role": "system", "content": self.system_prompt_base}
        ]
        
        # Configuration
        self.entity_noun_limit = entity_noun_limit
        self.similarity_threshold = similarity_threshold
        self.memory_recall_limit = memory_recall_limit
        self.max_context_messages = max_context_messages
        self.neutral_threshold = 0.1 
        
        # Caching & Performance
        self._entity_vector_cache = {}
        
        # NEW: Enhanced Memory Tracking
        self.conversation_themes = Counter()
        self.entity_frequency = Counter()
        self.sentiment_history = []
        self.last_memory_recall = []

    def chat(self, user_input: str) -> str:
        cmd_prefixes = ["!", "/"]
        is_command = any(user_input.strip().startswith(p) for p in cmd_prefixes)

        if not is_command:
            # 1. ENHANCED Memory Processing
            sentiment_score = self._get_sentiment(user_input)
            self.sentiment_history.append(sentiment_score)
            
            # Extract and track entities
            entities = self._extract_entities(user_input)
            
            # Only update frequency for meaningful entities
            if entities:
                self.entity_frequency.update(entities)
            
            # Process memory with theme tracking (only if entities exist)
            if entities:
                self._process_memory_entry(user_input, sentiment_score, entities)
            
            # 2. DYNAMIC Memory Recall with enhanced weighting
            recalled_memory = self._recall_relevant_memory(user_input)
            self.last_memory_recall = recalled_memory
            
            # 3. Build Context with Memory Injection
            messages_for_api = self._build_context_with_memory(user_input, recalled_memory)
            
            # Store user input permanently to conversation history
            self.messages.append({"role": "user", "content": user_input})
            
        else:
            # Command path - no memory processing
            messages_for_api = self.messages + [{"role": "user", "content": user_input}]
            self.messages.append({"role": "user", "content": user_input})

        # Get reply from the external API connector
        reply = send_message(messages_for_api) 
        
        if reply:
            self.messages.append({"role": "assistant", "content": reply})
            
            # NEW: Track themes in AI responses
            self._extract_themes(reply)
            
            # Prune context if too long
            self._prune_context()
            
            # Save context
            self.memory.save_context(self.messages)

        return reply

    def _build_context_with_memory(self, user_input: str, recalled_memory: list) -> list:
        """
        Build API messages with dynamically injected memory context.
        """
        messages_for_api = self.messages.copy() 
        
        dynamic_system_prompt = self.system_prompt_base
        
        if recalled_memory:
            memory_string = self._format_memory_for_prompt(recalled_memory)
            dynamic_system_prompt += f"\n\n**USER MEMORY CONTEXT:**\n{memory_string}"
            
            # Add emotional arc if significant
            emotional_context = self._get_emotional_arc_summary()
            if emotional_context:
                dynamic_system_prompt += f"\n\n**EMOTIONAL ARC:**\n{emotional_context}"
            
            # Add theme evolution if significant
            theme_context = self._get_theme_summary()
            if theme_context:
                dynamic_system_prompt += f"\n\n**RECURRING THEMES:**\n{theme_context}"
        
        messages_for_api[0] = {"role": "system", "content": dynamic_system_prompt}
        messages_for_api.append({"role": "user", "content": user_input})
        
        return messages_for_api

    def _prune_context(self):
        """
        Keep context window manageable by removing old messages.
        Keeps system prompt + recent messages.
        """
        if len(self.messages) > self.max_context_messages:
            # Keep system prompt + last N messages
            system_msg = self.messages[0]
            recent_messages = self.messages[-(self.max_context_messages-1):]
            self.messages = [system_msg] + recent_messages
            logging.debug(f"Context pruned to {len(self.messages)} messages")

    # --- ENHANCED MEMORY RECALL ---

    def _recall_relevant_memory(self, user_input: str) -> list:
        """
        Enhanced memory recall with multi-factor weighting.
        Fixed to handle empty vectors gracefully.
        """
        user_doc = nlp(user_input)
        
        # FIX: Check if user_doc has a valid vector
        if not user_doc.has_vector or user_doc.vector_norm == 0:
            logging.debug(f"User input '{user_input}' has no valid vector, skipping memory recall")
            return []
        
        memory_data = self.memory.get_memory_data()
        scored_entries = []
        
        for entity_key, entry in memory_data.items():
            # Filter non-memory entries (metadata)
            if not isinstance(entry, dict) or entity_key.startswith("_"):
                continue

            try:
                # Use the caching method
                entity_doc = self._get_entity_doc(entity_key)
                
                # FIX: Check if entity has a valid vector before comparison
                if not entity_doc.has_vector or entity_doc.vector_norm == 0:
                    logging.debug(f"Entity '{entity_key}' has no valid vector, skipping")
                    continue
                
                # Suppress RuntimeWarning from SpaCy 
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    similarity = user_doc.similarity(entity_doc)
                    
            except (ValueError, TypeError, RuntimeWarning) as e:
                logging.debug(f"Similarity failed for '{entity_key}': {e}")
                continue

            # ENHANCED WEIGHTING FORMULA
            mem_score = entry.get("score", 0)
            frequency = self.entity_frequency.get(entity_key, 0)
            
            # Base: Similarity * (1 + |Sentiment|)
            base_score = similarity * (1 + math.fabs(mem_score))
            
            # Boost: Frequency (more mentioned = more relevant)
            frequency_boost = 1 + (frequency * 0.1)
            
            # Final weighted score
            weighted_score = base_score * frequency_boost

            if similarity >= self.similarity_threshold or weighted_score > self.similarity_threshold:
                scored_entries.append((
                    entity_key, 
                    weighted_score, 
                    entry, 
                    similarity,
                    frequency
                ))
        
        # Sort by weighted score descending
        scored_entries.sort(key=lambda x: x[1], reverse=True)
        
        return scored_entries[:self.memory_recall_limit]

    def _format_memory_for_prompt(self, recalled_memory: list) -> str:
        """
        Formats recalled memories for LLM injection with rich context.
        """
        if not recalled_memory:
            return ""

        formatted_memories = []
        
        # Recalled memory now contains: (entity, weighted_score, entry, similarity, frequency)
        for entity, weighted_score, entry, similarity, frequency in recalled_memory:
            mem_type = entry.get("type", "fact")
            score = entry.get("score", 0)
            
            # Determine label
            if mem_type == "preference":
                if score > self.neutral_threshold:
                    label = "a beloved interest" 
                elif score < -self.neutral_threshold:
                    label = "something disliked"
                else:
                    label = "a neutral topic"
            elif mem_type == "sentiment":
                if score > self.neutral_threshold:
                    label = "positive memory"
                elif score < -self.neutral_threshold:
                    label = "difficult memory"
                else:
                    label = "neutral memory"
            else:
                label = "known fact"

            # Add frequency context
            freq_note = f"mentioned {frequency}x" if frequency > 1 else "new"

            formatted_memories.append(
                f"'{entity}': {label} ({freq_note}, "
                f"sentiment: {score:+.2f}, relevance: {similarity:.2f})"
            )

        # Use structured bullet points for the LLM
        return "\n".join([f"- {m}" for m in formatted_memories])

    # --- THEME & EMOTIONAL TRACKING ---

    def _extract_themes(self, text: str):
        """Extract and track gothic/narrative themes from text."""
        text_lower = text.lower()
        
        gothic_themes = [
            "darkness", "shadow", "light", "death", "spirit", "ghost",
            "memory", "sorrow", "loneliness", "beauty", "art", "creation",
            "haunting", "whisper", "silence", "ink", "tears", "wind",
            "night", "moon", "blood", "soul", "dream", "fear"
        ]
        
        for theme in gothic_themes:
            if theme in text_lower:
                self.conversation_themes[theme] += 1

    def _get_theme_summary(self, top_n=3) -> str:
        """Get summary of most common themes."""
        if not self.conversation_themes:
            return ""
        
        top_themes = self.conversation_themes.most_common(top_n)
        theme_str = ", ".join([f"{theme} ({count}x)" for theme, count in top_themes])
        return f"Recurring motifs: {theme_str}"

    def _get_emotional_arc_summary(self) -> str:
        """Analyze emotional trajectory of conversation."""
        if len(self.sentiment_history) < 3:
            return ""
        
        recent = self.sentiment_history[-5:]
        avg_sentiment = sum(recent) / len(recent)
        
        if avg_sentiment > 0.3:
            arc = "predominantly positive"
        elif avg_sentiment < -0.3:
            arc = "increasingly melancholic"
        else:
            arc = "emotionally balanced"
        
        return f"Emotional tone: {arc} (avg: {avg_sentiment:+.2f})"

    # --- Memory Management and Display ---

    def get_context(self):
        """Return current conversation context."""
        return self.messages

    def get_memory_summary(self, top_n=5):
        """Prepares and returns structured data for memory display with enhanced metrics."""
        
        metadata = self.memory.get_memory_metadata() 
        has_context = bool(self.memory.load_context())
        likes, dislikes = [], []

        for key, value in self.memory.get_memory_data().items():
            if not isinstance(value, dict) or key.startswith("_"):
                continue
            score = value.get("score", 0)
            if score > self.neutral_threshold:
                likes.append((key, score))
            elif score < -self.neutral_threshold:
                dislikes.append((key, score))

        likes.sort(key=lambda x: x[1], reverse=True)
        dislikes.sort(key=lambda x: x[1])

        def build_table(title, data, color="green"):
            table = Table(title=title, title_style=f"bold {color}", header_style=f"bold {color}")
            table.add_column("Entity", style="cyan", no_wrap=True)
            table.add_column("Score", style="magenta", justify="right")
            table.add_column("Frequency", style="yellow", justify="right")
            
            if data:
                for name, score in data[:top_n]:
                    freq = self.entity_frequency.get(name, 0)
                    table.add_row(name, f"{score:.2f}", f"{freq}x")
            else:
                table.add_row("None yet", "-", "-")
            return table

        likes_table = build_table("Top Preferences", likes, "green")
        dislikes_table = build_table("Top Dislikes", dislikes, "red")

        return {
            "total_entries": metadata["total_entries"],
            "last_updated": metadata["last_updated"],
            "has_context": has_context,
            "likes_table": likes_table,
            "dislikes_table": dislikes_table,
            "theme_summary": self._get_theme_summary(),
            "emotional_arc": self._get_emotional_arc_summary(),
            "total_themes": len(self.conversation_themes),
            "total_entities": len(self.entity_frequency)
        }

    def clear_memory(self):
        """Wipe all stored memory (permanent reset)."""
        self.memory.clear_memory()
        self.conversation_themes.clear()
        self.entity_frequency.clear()
        self.sentiment_history.clear()
        self.last_memory_recall.clear()

    def reset_context(self):
        """Reset conversation context — reset to system prompt."""
        self.messages = [{"role": "system", "content": self.system_prompt_base}]
        self.memory.clear_context()

    def reset_all(self):
        """Reset memory and context."""
        self.clear_memory()
        self.reset_context()

    # --- Entity & Sentiment Processing ---
    
    def _get_entity_doc(self, entity_key: str):
        """Retrieves or creates the SpaCy Doc for an entity, using a cache."""
        if entity_key not in self._entity_vector_cache:
            self._entity_vector_cache[entity_key] = nlp(entity_key)
        return self._entity_vector_cache[entity_key]

    def _extract_entities(self, text: str) -> list:
        """Extract entities (PERSON, WORK_OF_ART, etc.) and fallback to key nouns."""
        
        entities = set() 
        doc = nlp(text)
        
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON", "WORK_OF_ART", "PRODUCT", "EVENT"]:
                entities.add(ent.text)
                
        nouns = [
            token.text 
            for token in doc 
            if token.pos_ in ["NOUN", "PROPN"] 
            and token.text.lower() not in ["thing", "stuff", "it", "something"]
            and len(token.text) > 2
        ]
        
        for noun in nouns:
            entities.add(noun)
            
        return list(entities)[:self.entity_noun_limit]

    def _get_sentiment(self, text: str) -> float:
        """Get sentiment score from TextBlob."""
        blob = TextBlob(text)
        return max(-1.0, min(1.0, blob.sentiment.polarity))

    def _process_memory_entry(self, text: str, sentiment_score: float, entities: list):
        """Extract preferences/dislikes and save to memory with enhanced context."""
        keywords = self._get_keywords(text.lower())
        
        for entity in entities:
            entry_data = {
                "type": "preference" if keywords else "sentiment",
                "text": text[:200],
                "score": sentiment_score,
                "timestamp": datetime.now().isoformat(),
                "keywords": keywords
            }
            
            self.memory.set_memory_entry(entity, entry_data)
            
            # Clear cache entry for this entity if it exists
            if entity in self._entity_vector_cache:
                del self._entity_vector_cache[entity]

    def _get_keywords(self, text: str) -> str:
        """Return 'like' or 'dislike' based on keywords."""
        like_keywords = ["like", "love", "enjoy", "favorite", "interested in", "keen on", "fond of", "admire", "adore", "prefer"]
        dislike_keywords = ["dislike", "hate", "not a fan", "avoid", "detest", "can't stand", "loathe"]
        
        for kw in like_keywords:
            if kw in text:
                return "like"
        for kw in dislike_keywords:
            if kw in text:
                return "dislike"
        return None
            
    # Similarity helpers (unused but kept for compatibility)
    def _get_keywords_doc(self, keywords):
        """Convert keyword list to spacy Doc for similarity."""
        return [nlp(k) for k in keywords]

    def _get_keywords_similarity(self, text: str, keywords: list) -> bool:
        """Check if text is similar to any keyword."""
        doc = nlp(text)
        for keyword in keywords:
            if any(token.similarity(keyword) >= self.similarity_threshold for token in doc):
                return True
        return False