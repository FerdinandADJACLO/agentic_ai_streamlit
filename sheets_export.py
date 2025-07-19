import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Define sheet info
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Your downloaded file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1LLcUjXOs0R0fs79Zayq0l16a7mWtgBRnkpnb6XJrQik'
SHEET_RANGE = 'Sheet1!A1'  # Or wherever you want to write

# Authenticate
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Function to export
def export_agent_memory(memory_entries, platform):
    values = [["Platform", "Theme", "Idea", "Timestamp"]]
    for entry in memory_entries:
        values.append([
            platform,
            entry["theme"],
            entry["idea"],
            entry["timestamp"]
        ])

    body = {"values": values}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"✅ {result.get('updatedCells')} cells updated in Google Sheets.")
    import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

# 🧾 File-based memory or calendar entries to export
MEMORY_FILE = "memory_store.json"       # or use "calendar_plan.json" for calendar export
SERVICE_ACCOUNT_FILE = "credentials.json"
SPREADSHEET_ID = "1LLcUjXOs0R0fs79Zayq0l16a7mWtgBRnkpnb6XJrQik"
RANGE_NAME = "Sheet1!A1"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def load_memory(platform):
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    return memory.get(platform, [])

def prepare_memory_data(entries, platform):
    data = [["Platform", "Theme", "Idea", "Timestamp"]]
    for entry in entries:
        data.append([
            platform,
            entry.get("theme", ""),
            entry.get("idea", ""),
            entry.get("timestamp", "")
        ])
    return data

def export_to_google_sheets(values):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    body = {"values": values}

    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"✅ Exported {result.get('updatedCells')} cells to Google Sheets.")

# ✨ You can now call this from agent_script.py or run it directly:
if __name__ == "__main__":
    platform = input("Which platform memory would you like to export (TikTok/LinkedIn)? ").strip()
    entries = load_memory(platform)
    values = prepare_memory_data(entries, platform)
    export_to_google_sheets(values)