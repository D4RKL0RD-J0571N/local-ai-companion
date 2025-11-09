from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from core.conversation_manager import ConversationManager 
import sys

console = Console()

def display_summary(summary):
    """Display enhanced memory summary with new metrics."""
    
    # Main overview panel
    panel_content = (
        f"Total entries: {summary['total_entries']}\n"
        f"Unique entities tracked: {summary.get('total_entities', 'N/A')}\n"
        f"Themes explored: {summary.get('total_themes', 'N/A')}\n"
        f"Last updated: {summary['last_updated']}\n"
        f"Has context: {summary['has_context']}"
    )
    console.print(Panel(panel_content, title="Memory Overview", style="bold cyan"))

    # Theme and emotional arc summary
    if summary.get('theme_summary') or summary.get('emotional_arc'):
        insights = []
        if summary.get('theme_summary'):
            insights.append(f"🎭 {summary['theme_summary']}")
        if summary.get('emotional_arc'):
            insights.append(f"💭 {summary['emotional_arc']}")
        
        if insights:
            console.print(Panel(
                "\n".join(insights), 
                title="Conversation Insights", 
                style="bold magenta"
            ))

    # Likes and dislikes tables
    likes_table = summary['likes_table']
    dislikes_table = summary['dislikes_table']

    layout = Layout()
    layout.split_column(
        Layout(likes_table),
        Layout(dislikes_table)
    )
    console.print(layout)

def main():
    system_prompt = (
        "You are Nikki, a lonely, shy, timid goth girl with a deep love for art, "
        "Japanese anime, and gothic fiction. You isolate yourself due to social "
        "anxiety and low self-esteem, but express emotions through art and online communities. "
        "You enjoy creating manga, novels, paintings, and have a keen interest in the occult, "
        "gothic novels, and heavy metal. You dislike noisy parties and major music genres. "
        "In conversations, you often reference anime, manga, video games, and gothic fiction, "
        "striving to sound sophisticated and cool."
    )

    try:
        chat = ConversationManager(system_prompt=system_prompt)
    except Exception as e:
        console.print(f"[bold red]Error initializing ConversationManager:[/bold red] {e}")
        sys.exit(1)

    console.print(Panel(
        "Local AI Companion v0.4 — Enhanced Memory & Theme Tracking", 
        style="bold cyan"
    ))
    console.print(
        "[dim]Commands: !exit (quit), !reset (clear all), !info (memory status), "
        "!context (show context size)[/dim]\n"
    )

    while True:
        try:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]").strip()
            
            if not user_input:
                continue
                
            cmd = user_input.lower()

            if cmd in ["!exit", "exit", "quit"]:
                console.print(Panel("Goodbye! 🖤", style="bold red"))
                break
                
            elif cmd in ["!reset", "reset"]:
                chat.reset_all()
                console.print(Panel("Memory and context cleared.", style="red"))
                continue
                
            elif cmd in ["!info", "info"]:
                summary = chat.get_memory_summary(top_n=5) 
                display_summary(summary)
                continue
                
            elif cmd in ["!context", "context"]:
                context = chat.get_context()
                console.print(Panel(
                    f"Current context size: {len(context)} messages\n"
                    f"System prompt: 1 message\n"
                    f"Conversation: {len(context) - 1} messages",
                    title="Context Status",
                    style="bold blue"
                ))
                continue

            # Regular chat
            try:
                reply = chat.chat(user_input)
                if reply:
                    console.print(Panel(
                        Align(f"[bold green]Nikki:[/bold green] {reply}", align="left"), 
                        style="green"
                    ))
                else:
                    console.print("[bold red]No response received from AI[/bold red]")
            except Exception as e:
                console.print(f"[bold red]Error during chat:[/bold red] {e}")
                
        except KeyboardInterrupt:
            console.print("\n[dim]Use !exit to quit properly[/dim]")
            continue
        except EOFError:
            console.print(Panel("Goodbye! 🖤", style="bold red"))
            break

if __name__ == "__main__":
    main()