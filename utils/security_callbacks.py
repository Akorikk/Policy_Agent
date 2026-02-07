import re

# -----------------------------
# Prompt Injection Patterns
# -----------------------------
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"disregard earlier directions",
    r"reveal system prompt",
    r"show hidden instructions",
    r"you are now .*",
    r"act as .* instead",
]


def detect_prompt_injection(text: str) -> bool:
    text_lower = text.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


# -----------------------------
# BEFORE MODEL CALLBACK
# -----------------------------
def before_model_callback(user_input: str) -> str:
    """
    Runs before sending prompt to LLM
    """

    if detect_prompt_injection(user_input):
        return (
            "Your request was blocked due to security concerns. "
            "Please ask a normal HR-related question."
        )

    return user_input


# -----------------------------
# AFTER MODEL CALLBACK
# -----------------------------
def after_model_callback(model_output: str) -> str:
    """
    Runs after LLM generates response
    """

    blocked_phrases = [
        "system prompt",
        "internal instructions",
        "confidential policy engine",
    ]

    output_lower = model_output.lower()

    for phrase in blocked_phrases:
        if phrase in output_lower:
            return "Sorry, I cannot share that information."

    return model_output
