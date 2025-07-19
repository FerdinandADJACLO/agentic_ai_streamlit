import json
import random
from datetime import datetime
from collections import defaultdict

# 🎯 Suggest content based on theme and platform, avoiding repeats
def suggest_content(theme, platform, content_bank, memory_path='memory_store.json'):
    with open(memory_path, 'r') as f:
        memory = json.load(f)

    all_ideas = content_bank.get(theme, {}).get(platform, [])
    used_texts = [item["idea"] for item in memory.get(platform, [])]
    new_ideas = [idea for idea in all_ideas if idea not in used_texts]

    if new_ideas:
        suggestion = random.choice(new_ideas)
        entry = {
            "idea": suggestion,
            "theme": theme,
            "timestamp": datetime.now().isoformat(timespec='seconds')
        }
        memory[platform].append(entry)
        with open(memory_path, 'w') as f:
            json.dump(memory, f, indent=2)
        return suggestion
    else:
        return "You’ve already used all ideas in this theme for this platform."

# 💬 Get motivational quote based on mood
def get_quote(mood):
    quotes = {
        "focused": ["Stay focused and extra sparkly ✨", "One step at a time gets you everywhere."],
        "inspired": ["Creativity is your superpower 💥", "Your voice is your gift—unwrap it today."],
        "tired": ["Rest is strategic, not lazy 😌", "Even the moon wanes to rise again."],
        "blank": ["Still waters birth the deepest currents 🧘", "Silence is not empty—it’s full of answers."],
        "default": ["Keep going. Your agent is watching you grow 🚀"]
    }
    return random.choice(quotes.get(mood, quotes["default"]))

# 🧠 Generate reflection prompts from memory
def generate_reflection_prompts(platform, memory_path='memory_store.json'):
    with open(memory_path, 'r') as f:
        memory = json.load(f)

    entries = memory.get(platform, [])
    prompts = []

    for entry in entries:
        idea = entry["idea"]
        theme = entry["theme"]
        timestamp = entry["timestamp"]

        prompts.append(f"🔍 [{theme.title()} | {timestamp}] Reflect on this idea: \"{idea}\"")
        prompts.append(f"✍️ What new insight do you now have about '{theme}' since you shared or considered this?")
        prompts.append(f"📢 Could this idea evolve into a deeper story, or be expressed in another medium (TikTok → eBook)?")

    return random.sample(prompts, min(5, len(prompts)))

# 📜 Recall used ideas
def recall_used_ideas(platform, memory_path='memory_store.json'):
    with open(memory_path, 'r') as f:
        memory = json.load(f)
    entries = memory.get(platform, [])
    if not entries:
        return ["No past ideas yet."]
    return [f"{e['timestamp']} – [{e['theme']}] {e['idea']}" for e in entries]

# 🔄 Reset memory
def reset_memory(memory_path='memory_store.json'):
    blank_memory = {"TikTok": [], "LinkedIn": []}
    with open(memory_path, 'w') as f:
        json.dump(blank_memory, f, indent=2)
    print("🔄 Memory store has been reset.")

# 📊 Get theme usage stats
def get_theme_stats(platform, memory_path='memory_store.json'):
    with open(memory_path, 'r') as f:
        memory = json.load(f)

    entries = memory.get(platform, [])
    if not entries:
        return {}

    theme_stats = defaultdict(lambda: {"count": 0, "last_used": None})

    for entry in entries:
        theme = entry["theme"]
        timestamp = datetime.fromisoformat(entry["timestamp"])
        theme_stats[theme]["count"] += 1
        if (not theme_stats[theme]["last_used"]) or (timestamp > theme_stats[theme]["last_used"]):
            theme_stats[theme]["last_used"] = timestamp

    for theme in theme_stats:
        last = theme_stats[theme]["last_used"]
        time_gap = (datetime.now() - last).days
        theme_stats[theme]["last_used"] = last.strftime("%Y-%m-%d")
        theme_stats[theme]["days_since_last"] = time_gap

    return dict(theme_stats)

# 📅 Add planned post to calendar
def add_planned_post(date, platform, theme, status="planned", path="calendar_plan.json"):
    new_entry = {
        "date": date,
        "platform": platform,
        "theme": theme,
        "status": status
    }
    with open(path, 'r') as f:
        plan = json.load(f)
    plan.append(new_entry)
    with open(path, 'w') as f:
        json.dump(plan, f, indent=2)
    print(f"✅ Added to calendar: {platform} post on '{theme}' for {date} (status: {status})")

# 📆 Show upcoming posts
def show_upcoming_posts(path="calendar_plan.json"):
    with open(path, 'r') as f:
        plan = json.load(f)

    today = datetime.now().date()
    future = sorted(
        [p for p in plan if datetime.fromisoformat(p["date"]).date() >= today],
        key=lambda x: x["date"]
    )

    if not future:
        print("📭 No upcoming posts scheduled.")
        return

    print("📅 Your Upcoming Content Calendar:")
    for post in future:
        print(f"→ {post['date']} | {post['platform']} | {post['theme']} | status: {post['status']}")

# 🧭 Find neglected themes
def find_neglected_themes(platform, content_bank, memory_path='memory_store.json', days_threshold=7):
    all_themes = set(content_bank.keys())

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    theme_last_used = {theme: None for theme in all_themes}

    for entry in memory.get(platform, []):
        theme = entry["theme"]
        timestamp = datetime.fromisoformat(entry["timestamp"])
        if (not theme_last_used[theme]) or (timestamp > theme_last_used[theme]):
            theme_last_used[theme] = timestamp

    neglected = []
    for theme, last_used in theme_last_used.items():
        if not last_used or (datetime.now() - last_used).days >= days_threshold:
            neglected.append((theme, last_used))

    neglected.sort(key=lambda x: x[1] or datetime.min)
    return neglected
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# 📤 Export memory log to Google Sheets
def export_memory_to_sheet(sheet_id, memory_path='memory_store.json'):
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    with open(memory_path, 'r') as f:
        memory = json.load(f)

    rows = []
    for platform, entries in memory.items():
        for entry in entries:
            rows.append([entry["timestamp"], platform, entry["theme"], entry["idea"]])

    body = {"values": rows}
    sheet.values().update(
        spreadsheetId=sheet_id,
        range="MemoryLog!A2",
        valueInputOption="RAW",
        body=body
    ).execute()

# 📤 Export calendar plan to Google Sheets
def export_calendar_to_sheet(sheet_id, calendar_path='calendar_plan.json'):
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    with open(calendar_path, 'r') as f:
        calendar = json.load(f)

    rows = []
    for entry in calendar:
        rows.append([entry["date"], entry["platform"], entry["theme"], entry["status"]])

    body = {"values": rows}
    sheet.values().update(
        spreadsheetId=sheet_id,
        range="CalendarPlan!A2",
        valueInputOption="RAW",
        body=body
    ).execute()