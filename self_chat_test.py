import time
import random
from collections import deque
from difflib import SequenceMatcher
from core.conversation_manager import ConversationManager
from rich.console import Console

console = Console()

def calculate_similarity(str1, str2):
    """Calculate similarity ratio between two strings (0.0 to 1.0)"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def table_to_text(table):
    """
    Converts a Rich Table object into a plain text string for logging.
    """
    if not hasattr(table, 'rows') or not table.rows:
        return "  - None yet.\n"
    
    output_lines = []
    for row in table.rows:
        # row.cells contains each column value
        output_lines.append(f"  - {row.cells[0]}: {row.cells[1]} (freq: {row.cells[2]})")
    return "\n".join(output_lines) + "\n"

class ThemeEvolution:
    """Tracks and evolves gothic narrative themes across conversation."""
    
    def __init__(self):
        self.themes = []
        self.theme_keywords = {
            "lantern": ["light", "darkness", "flame", "guide", "hope"],
            "shrine": ["sacred", "worship", "spirit", "memory", "devotion"],
            "tears": ["sorrow", "emotion", "grief", "sadness", "loss"],
            "ink": ["writing", "creation", "permanence", "story", "mark"],
            "wind": ["whisper", "breath", "movement", "unseen", "change"],
            "spirit": ["ghost", "haunt", "presence", "soul", "ethereal"],
            "shadow": ["darkness", "hidden", "mystery", "fear", "depth"],
            "moon": ["night", "pale", "reflection", "cycle", "beauty"]
        }
        
    def add_theme(self, theme_name):
        """Add a new theme to the evolution tracker."""
        if theme_name not in self.themes:
            self.themes.append(theme_name)
            
    def get_evolution_summary(self):
        """Get a summary of theme progression."""
        if not self.themes:
            return "No themes explored yet."
        return " → ".join(self.themes)
    
    def suggest_next_theme(self):
        """Suggest a new gothic theme based on what's been explored."""
        unused_themes = [t for t in self.theme_keywords.keys() if t not in self.themes]
        if unused_themes:
            return random.choice(unused_themes)
        return random.choice(list(self.theme_keywords.keys()))

def self_chat_with_memory_tables(
    turns=100, 
    delay=0.2, 
    history_size=5,  # Increased from 3 for better loop detection
    snapshot_interval=50,
    similarity_threshold=0.85  # NEW: Detect near-duplicate responses (85%+ similar)
):
    """
    Enhanced self-chat simulation with:
    - Improved loop detection (semantic similarity)
    - Theme evolution tracking
    - Better memory prompt variety
    - Duplicate prompt prevention
    - Actual API integration
    """
    
    system_prompt = (
        "You are Nikki, a lonely, shy, timid goth girl with a deep love for art, "
        "Japanese anime, and gothic fiction. You enjoy creating manga, novels, paintings, "
        "and have a keen interest in the occult, gothic novels, and heavy metal. "
        "Maintain a complex personality and each turn, refer back to something specific "
        "from the past while introducing a related new topic. Be creative and avoid "
        "repeating the same phrases or ideas. Vary your responses and explore different "
        "aspects of gothic themes."
    )

    chat = ConversationManager(system_prompt=system_prompt)
    theme_tracker = ThemeEvolution()

    initial_user_input = "Hello Nikki. Let's start a deep conversation about gothic art and stories. What's one thing you are currently obsessed with?"
    
    reply_history = deque(maxlen=history_size)
    prompt_history = deque(maxlen=history_size)  # NEW: Track used prompts to avoid repetition
    user_input = initial_user_input

    console.print("\n[bold cyan]--- Starting Enhanced Self-Chat Simulation ---[/bold cyan]")
    console.print(f"[dim]Turns: {turns} | Loop Detection: {similarity_threshold:.0%} | History Size: {history_size}[/dim]\n")

    with open("self_chat_log.txt", "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write("ENHANCED SELF-CHAT LOG\n")
        f.write("="*70 + "\n")
        f.write(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Theme Evolution Enabled: Yes\n")
        f.write(f"Loop Detection Threshold: {similarity_threshold:.0%}\n")
        f.write(f"History Size: {history_size}\n")
        f.write("="*70 + "\n\n")
        
        for i in range(1, turns + 1):
            start_time = time.time()

            # --- ENHANCED PROMPT GENERATION ---
            if i % 5 == 0 and i > 5:
                # Memory recall prompts with theme evolution
                memory_prompts = [
                    "Recall one gothic element you mentioned earlier and deepen it with new symbolism.",
                    "What's the most haunting emotion you've described? Transform it into a new scene.",
                    "Take a theme from your memory and reimagine it in a different gothic setting.",
                    "Blend two things you've mentioned into an unexpected gothic metaphor.",
                    f"Introduce the theme of '{theme_tracker.suggest_next_theme()}' into your narrative.",
                    "What memory from our conversation still lingers? Explore its shadow side.",
                    "Retrieve a forgotten detail from earlier and breathe new life into it."
                ]
                next_user_input = random.choice(memory_prompts)
                stress_tag = " [MEMORY+EVOLUTION]"
                
            else:
                # Variation prompts that encourage divergent thinking
                variation_prompts = [
                    f"Transform this idea into visual gothic imagery: '{user_input[:40]}'",
                    f"What shadows hide beneath: '{user_input[:40]}'?",
                    f"Shift perspective: if '{user_input[:40]}' were a character, who would they be?",
                    f"Create a gothic paradox from: '{user_input[:40]}'",
                    f"Weave darkness into: '{user_input[:40]}'",
                    "Take your last thought and twist it into something unexpected.",
                    "What's the opposite gothic interpretation of what you just said?",
                    "If your last statement were a painting, what would be in the background?"
                ]
                next_user_input = random.choice(variation_prompts)
                stress_tag = ""

            # --- DUPLICATE PROMPT PREVENTION ---
            # If we've used this exact prompt recently, generate an alternative
            if next_user_input in prompt_history:
                next_user_input = f"Evolve your last thought with an unexpected gothic twist that surprises even you."
                stress_tag += " [ALT]"
            
            prompt_history.append(next_user_input)

            # --- CONVERSATION TURN ---
            reply = chat.chat(next_user_input)
            end_time = time.time()
            duration = end_time - start_time

            # --- ENHANCED LOOP DETECTION ---
            loop_detected = False
            max_similarity = 0.0
            
            for prev_reply in reply_history:
                similarity = calculate_similarity(reply.strip(), prev_reply)
                max_similarity = max(max_similarity, similarity)
                
                if similarity > similarity_threshold:
                    loop_detected = True
                    f.write("\n" + "="*70 + "\n")
                    f.write(f"!!! SEMANTIC LOOP DETECTED at Turn {i} !!!\n")
                    f.write("="*70 + "\n")
                    f.write(f"Current reply similarity: {similarity:.2%}\n")
                    f.write(f"Matches previous response in history.\n")
                    f.write(f"Theme Evolution: {theme_tracker.get_evolution_summary()}\n")
                    f.write("="*70 + "\n\n")
                    
                    console.print(f"\n[bold red]⚠️  LOOP DETECTED at Turn {i}[/bold red]")
                    console.print(f"[yellow]Similarity: {similarity:.2%}[/yellow]")
                    console.print(f"[cyan]Theme Evolution: {theme_tracker.get_evolution_summary()}[/cyan]\n")
                    break
            
            if loop_detected:
                break

            # --- LOGGING CONVERSATION ---
            context_length = len(chat.get_context())
            
            f.write("─"*70 + "\n")
            f.write(f"Turn {i}{stress_tag}\n")
            f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} | ")
            f.write(f"Duration: {duration:.2f}s | Context: {context_length} | ")
            f.write(f"Max Similarity: {max_similarity:.2%}\n")
            f.write("─"*70 + "\n")
            f.write(f"User: {next_user_input}\n\n")
            f.write(f"Nikki: {reply}\n\n")

            # Console output (condensed)
            console.print(f"[bold cyan]Turn {i:3d}[/bold cyan]{stress_tag} [dim]({duration:.2f}s)[/dim]")
            console.print(f"  [yellow]User:[/yellow] {next_user_input[:65]}{'...' if len(next_user_input) > 65 else ''}")
            console.print(f"  [green]Nikki:[/green] {reply[:65]}{'...' if len(reply) > 65 else ''}")
            console.print()

            # --- THEME EXTRACTION ---
            reply_lower = reply.lower()
            for theme in theme_tracker.theme_keywords.keys():
                if theme in reply_lower or any(kw in reply_lower for kw in theme_tracker.theme_keywords[theme]):
                    theme_tracker.add_theme(theme)

            # --- MEMORY SNAPSHOT ---
            if i % snapshot_interval == 0:
                summary = chat.get_memory_summary(top_n=5)
                
                f.write("\n" + "="*70 + "\n")
                f.write(f"MEMORY SNAPSHOT - Turn {i}\n")
                f.write("="*70 + "\n")
                f.write(f"Total Entries: {summary['total_entries']} | ")
                f.write(f"Last Updated: {summary['last_updated']}\n")
                f.write(f"Total Unique Entities: {summary['total_entities']}\n")
                f.write(f"Total Themes Tracked: {summary['total_themes']}\n\n")
                
                if summary.get('theme_summary'):
                    f.write(f"Theme Evolution: {theme_tracker.get_evolution_summary()}\n")
                    f.write(f"{summary['theme_summary']}\n\n")
                
                if summary.get('emotional_arc'):
                    f.write(f"{summary['emotional_arc']}\n\n")
                
                f.write("Top Likes:\n")
                f.write(table_to_text(summary['likes_table']))
                f.write("\nTop Dislikes:\n")
                f.write(table_to_text(summary['dislikes_table']))
                f.write("="*70 + "\n\n")
                
                console.print(f"[bold magenta]📊 Memory snapshot logged at Turn {i}[/bold magenta]")
                console.print(f"[cyan]🎭 Themes: {theme_tracker.get_evolution_summary()}[/cyan]")
                if summary.get('emotional_arc'):
                    console.print(f"[yellow]{summary['emotional_arc']}[/yellow]")
                console.print()

            # --- UPDATE HISTORY ---
            reply_history.append(reply.strip())
            user_input = reply
            
            time.sleep(delay)
        
        # --- FINAL SUMMARY ---
        f.write("\n" + "="*70 + "\n")
        f.write("SIMULATION COMPLETE\n")
        f.write("="*70 + "\n")
        f.write(f"Total Turns Completed: {i}\n")
        f.write(f"Theme Evolution: {theme_tracker.get_evolution_summary()}\n")
        f.write(f"Ended: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Get final memory summary
        final_summary = chat.get_memory_summary(top_n=10)
        f.write(f"\nFinal Statistics:\n")
        f.write(f"- Total Memory Entries: {final_summary['total_entries']}\n")
        f.write(f"- Unique Entities Tracked: {final_summary['total_entities']}\n")
        f.write(f"- Themes Explored: {final_summary['total_themes']}\n")
        if final_summary.get('emotional_arc'):
            f.write(f"- {final_summary['emotional_arc']}\n")
        f.write("="*70 + "\n")

    console.print(f"\n[bold green]✅ Self-chat simulation complete[/bold green] [dim]({i} turns)[/dim]")
    console.print(f"[cyan]🎭 Theme evolution: {theme_tracker.get_evolution_summary()}[/cyan]")
    console.print(f"[yellow]📝 Log saved to 'self_chat_log.txt'[/yellow]\n")

if __name__ == "__main__":
    self_chat_with_memory_tables(
        turns=200, 
        delay=0.2,  # Delay between turns (adjust as needed)
        history_size=5,  # Track last 5 replies for loop detection
        snapshot_interval=50,  # Memory snapshot every 50 turns
        similarity_threshold=0.85  # Detect 85%+ similar responses as loops
    )