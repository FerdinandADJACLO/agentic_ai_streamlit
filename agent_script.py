import json
from datetime import datetime

# Load content bank
with open('content_bank.json', 'r') as f:
    content_bank = json.load(f)

# Initial output
print("✅ Content bank loaded successfully!")
from mood_logic import get_theme_from_mood
from utils import suggest_content, get_quote, add_planned_post
import json

# Load content bank
with open('content_bank.json', 'r') as f:
    content_bank = json.load(f)

# User input
mood = input("What’s your mood? (focused, inspired, tired, blank): ").lower()
platform = input("Which platform are you planning for? (TikTok/LinkedIn): ").capitalize()

# Agent reasoning
theme = get_theme_from_mood(mood)
idea = suggest_content(theme, platform, content_bank)
quote = get_quote(mood)

# Output
print(f"\n🎯 Theme based on your mood: {theme}")
print(f"📝 Suggested {platform} idea:\n→ {idea}")
print(f"\n💬 Inspirational Quote:\n→ {quote}")
from utils import suggest_content, get_quote
...

idea = suggest_content(theme, platform, content_bank, memory_path='memory_store.json')
recall = input("Do you want to review past suggestions? (yes/no): ").lower()
if recall == "yes":
    history = recall_used_ideas(platform)
    print("\n📜 Your creative memory log:")
    for entry in history:
        print("→", entry)
from utils import generate_reflection_prompts, recall_used_ideas

reflect = input("Would you like to reflect on past ideas? (yes/no): ").lower()

if reflect == "yes":
    prompts = generate_reflection_prompts(platform)
    print("\n🧘 Reflective Prompts:")
    for prompt in prompts:
        print(prompt)
        from utils import get_theme_stats

show_stats = input("Would you like to see your content dashboard? (yes/no): ").lower()
if show_stats == "yes":
    stats = get_theme_stats(platform)
    print(f"\n📈 Theme Usage for {platform}:")
    for theme, data in stats.items():
        print(f"→ {theme.title()}: used {data['count']} time(s), last on {data['last_used']} ({data['days_since_last']} day(s) ago)")
    plan = input("Want to schedule your next content idea? (yes/no): ").lower()

if plan == "yes":
    date = input("Enter target date (YYYY-MM-DD): ")
    platform = input("Platform (TikTok/LinkedIn): ").capitalize()
    theme = input("Planned theme (e.g. confidence, silence, resilience): ").lower()
    status = input("Status (planned/drafted/posted): ").lower()
    add_planned_post(date, platform, theme, status)

show = input("Want to review your calendar? (yes/no): ").lower()
from utils import show_upcoming_posts

if show == "yes":
    show_upcoming_posts() 
    from utils import find_neglected_themes

suggest = input("Want a strategic theme suggestion based on underuse? (yes/no): ").lower()
if suggest == "yes":
    neglected = find_neglected_themes(platform, content_bank)
    print("\n🧭 Themes you've touched the least:")
    for theme, last in neglected[:3]:
        ago = "never" if not last else f"{(datetime.now() - last).days} day(s) ago"
        print(f"→ {theme.title()} — last used: {ago}")
        from sheets_export import export_agent_memory

export = input("Export current memory to Google Sheets? (yes/no): ").lower()
if export == "yes":
    with open('memory_store.json', 'r') as f:
        memory = json.load(f)
    export_agent_memory(memory[platform], platform)