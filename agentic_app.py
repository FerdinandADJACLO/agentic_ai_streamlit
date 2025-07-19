import streamlit as st
import json
import random
from datetime import datetime
from mood_logic import get_theme_from_mood
from utils import (
    suggest_content, get_quote, add_planned_post,
    get_theme_stats, find_neglected_themes,
    export_memory_to_sheet, export_calendar_to_sheet
)

st.set_page_config(page_title="Agentic AI", layout="wide")
st.title("🧠 Agentic AI Content Companion")

# Load content bank
with open("content_bank.json", "r") as f:
    content_bank = json.load(f)

tab1, tab2, tab3 = st.tabs(["🎯 Content Generator", "🗂️ Theme Browser", "📊 Theme Insights"])

# 🎯 Tab 1: Content Generator
with tab1:
    st.subheader("Plan content based on your mood and platform")

    mood = st.selectbox("What's your mood?", [
        "focused", "inspired", "tired", "blank", "happy", "sad", "puzzled", "anxious",
        "excited", "bored", "grateful", "overwhelmed", "hopeful", "nostalgic", "confident", "playful"
    ], key="mood_selector_tab1")

    platform = st.selectbox("Choose your platform", ["TikTok", "LinkedIn"], key="platform_selector_tab1")

    if st.button("Generate Idea", key="generate_button_tab1"):
        theme = get_theme_from_mood(mood)
        idea = suggest_content(theme, platform, content_bank)
        quote = get_quote(mood)

        st.markdown(f"### 🎯 Theme: `{theme}`")
        st.markdown(f"**📝 Content Idea:** {idea}")
        st.markdown(f"**💬 Motivational Quote:** {quote}")

        with st.expander("📅 Schedule this idea"):
            date = st.date_input("Choose a date", key="date_input_tab1")
            status = st.selectbox("Status", ["planned", "drafted", "posted"], key="status_selector_tab1")
            if st.button("Add to Calendar", key="calendar_button_tab1"):
                add_planned_post(str(date), platform, theme, status)
                st.success("✅ Idea scheduled successfully!")

# 🗂️ Tab 2: Theme Browser
with tab2:
    st.subheader("Browse All Themes")

    if st.button("🎲 Surprise Me with a Random Theme", key="random_theme_button"):
        random_theme = random.choice(list(content_bank.keys()))
        st.success(f"✨ Try exploring: **{random_theme.title()}**")

    search = st.text_input("🔍 Search themes by keyword or mood", key="search_input_tab2").lower()

    matched_themes = {
        theme: ideas for theme, ideas in content_bank.items()
        if search in theme.lower() or any(search in idea.lower() for idea in ideas.get("TikTok", []) + ideas.get("LinkedIn", []))
    } if search else content_bank

    for theme, ideas in matched_themes.items():
        with st.expander(f"📌 {theme.title()}"):
            st.markdown("#### 🎥 TikTok Ideas")
            for idea in ideas.get("TikTok", []):
                st.markdown(f"- 🧠 {idea}")
            st.markdown("#### 💼 LinkedIn Ideas")
            for idea in ideas.get("LinkedIn", []):
                st.markdown(f"- 💡 {idea}")

# 📊 Tab 3: Theme Insights
with tab3:
    st.subheader("Theme Usage Insights")

    platform = st.selectbox("Select platform for stats", ["TikTok", "LinkedIn"], key="platform_selector_tab3")
    stats = get_theme_stats(platform)

    if stats:
        st.markdown("### 🔥 Theme Usage Heatmap")
        for theme, data in sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True):
            fire = "🔥" if data["count"] > 5 else "✨" if data["count"] > 2 else "🕸️"
            st.markdown(f"{fire} **{theme.title()}** – {data['count']} uses | Last used: `{data['last_used']}` | Days since: `{data['days_since_last']}`")
    else:
        st.info("No usage data yet. Start creating content!")

    st.markdown("### 🕳️ Neglected Themes")
    neglected = find_neglected_themes(platform, content_bank)
    for theme, last_used in neglected:
        last = last_used.strftime("%Y-%m-%d") if last_used else "Never"
        st.markdown(f"- **{theme.title()}** | Last used: {last}")

    st.markdown("---")
    st.subheader("📤 Export Data to Google Sheets")

    sheet_id = st.text_input("Enter your Google Sheet ID", key="sheet_id_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Memory Log", key="export_memory_button"):
            export_memory_to_sheet(sheet_id)
            sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid=0"
            st.success("✅ Memory exported successfully!")
            st.markdown(f"[🔗 Open Google Sheet]({sheet_url})")

    with col2:
        if st.button("Export Calendar Plan", key="export_calendar_button"):
            export_calendar_to_sheet(sheet_id)
            sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid=0"
            st.success("✅ Calendar exported successfully!")
            st.markdown(f"[🔗 Open Google Sheet]({sheet_url})")

# Footer
st.markdown("---")
st.markdown("🧠 *Agentic AI is your creative co-pilot. Every mood is a doorway. Every theme is a story waiting to be told.*")