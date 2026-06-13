def explain(text):
    text_lower = text.lower()
    reasons = []

    # punctuation
    if "!" in text:
        reasons.append("Excessive punctuation used")

    # curiosity phrases
    curiosity = [
        "you won't believe",
        "you won’t believe",
        "what happens next",
        "क्या हुआ",
        "जानकर रह जाएंगे"
    ]

    for c in curiosity:
        if c in text_lower:
            reasons.append(f"Curiosity phrase detected: {c}")

    # emotional words
    emotional = [
        "shocking", "unbelievable", "amazing", "incredible",
        "हैरान", "चौंक", "खुलासा", "सनसनी", "तहलका"
    ]

    for word in emotional:
        if word in text_lower:
            reasons.append(f"Emotional word detected: {word}")

    # ALL CAPS
    if text.isupper():
        reasons.append("All caps used (attention grabbing)")

    if not reasons:
        reasons.append("Neutral informational headline")

    return reasons