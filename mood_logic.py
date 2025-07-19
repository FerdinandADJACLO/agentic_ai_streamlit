import random

def get_theme_from_mood(mood):
    mood_to_themes = {
        "focused": ["confidence", "discipline", "clarity"],
        "inspired": ["creativity", "vision", "storytelling"],
        "tired": ["resilience", "simplicity", "reflection"],
        "blank": ["exploration", "curiosity", "learning"],
        "happy": ["joy", "connection", "playfulness"],
        "sad": ["authenticity", "healing", "legacy"],
        "puzzled": ["problem-solving", "perspective", "clarity"],
        "anxious": ["mindfulness", "support", "trust"],
        "excited": ["momentum", "boldness", "innovation"],
        "bored": ["novelty", "experimentation", "humor"],
        "grateful": ["gratitude", "community", "reflection"],
        "overwhelmed": ["simplicity", "focus", "balance"],
        "hopeful": ["growth", "vision", "purpose"],
        "nostalgic": ["memory", "heritage", "legacy"],
        "confident": ["leadership", "impact", "authenticity"],
        "playful": ["creativity", "humor", "connection"]
    }
    themes = mood_to_themes.get(mood.lower(), ["confidence"])
    return random.choice(themes)