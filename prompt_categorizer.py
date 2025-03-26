from difflib import SequenceMatcher
import re

CATEGORY_KEYWORDS = {
    "인물": [
        "girl", "boy", "man", "woman", "1girl", "1boy", "solo", "face", "smile",
        "portrait", "fang", "navel", "stomach", "small breasts", "breasts",
        "blue eyes", "yellow eyes", "pink hair", "long hair", "open mouth", "halo", "ahoge"
    ],
    "배경": [
        "forest", "room", "castle", "mountain", "landscape", "sky", "blue sky", "cloud",
        "sunset", "outdoors", "background", "airfield", "airplane_interior", "airport", "alley", "day"
    ],
    "스타일": [
        "anime", "realistic", "digital painting", "sketch", "artstyle",
        "masterpiece", "high quality", "best quality", "absurdres", "very aesthetic",
        "dynamic pose", "cinematic", "dramatic lighting", "photorealistic", "painting"
    ],
    "색감": [
        "vibrant", "monochrome", "pastel", "warm color", "cool color",
        "heterochromia", "two-tone", "colored lighting"
    ],
    "의상": [
        "dress", "kimono", "armor", "jacket", "school uniform", "suit",
        "costume", "clothing", "outfit", "cheerleader", "skirt", "miniskirt",
        "pleated skirt", "sideless_outfit", "topless", "pom pom", "white skirt",
        "Budget_sarashi", "Chest_sarashi", "Midriff_sarashi", "Sizes_of_panties",
        "cosplay", "millennium cheerleader outfit", "pom pom cheerleading"
    ],
    "행동": [
        "Angry_face", "Applying_makeup", "Biting", "Breathing", "Brushing_hair", "holding", "jumping"
    ],
    "자세": [
        "3/4_view", "Carrying_someone", "Hugging",
        "Hugging_doable_by_one_or_more_characters",
        "Hugging_doable_by_two_or_more_characters", "looking at viewer", "from"
    ]
}

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize_token(token):
    token = token.lower().strip()
    token = token.replace('-', ' ')
    token = re.sub(r"[^a-z0-9_ ]", "", token)
    return token

def clean_prompt(prompt: str):
    prompt = re.sub(r"[()\[\]{}]", "", prompt)  # 괄호 제거
    prompt = re.sub(r"\s+", " ", prompt)         # 공백 정리
    return prompt

def categorize_prompt(prompt: str, threshold=0.6):
    prompt = clean_prompt(prompt)
    tokens = [t.strip() for t in prompt.split(',') if t.strip()]
    result = {cat: [] for cat in CATEGORY_KEYWORDS}
    result["기타"] = []

    for token in tokens:
        norm_token = normalize_token(token)
        best_match = ("기타", 0)
        for category, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                norm_kw = normalize_token(kw)
                if norm_kw in norm_token:
                    best_match = (category, 1.0)
                    break
                sim = similarity(norm_token, norm_kw)
                if sim > best_match[1]:
                    best_match = (category, sim)
        if best_match[1] >= threshold:
            result[best_match[0]].append(token)
        else:
            result["기타"].append(token)

    return result

def format_categorized_prompt(categorized_dict):
    output = []
    for category, tokens in categorized_dict.items():
        if tokens:
            section = f"#{category}#\n" + ", ".join(tokens) + "\n"
            output.append(section)
    return "\n".join(output).strip()


class PromptCategorizer:
    CATEGORY_KEYWORDS = CATEGORY_KEYWORDS

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "threshold": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 1.0}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("categorized_prompt",)
    FUNCTION = "categorize"
    CATEGORY = "prompt_master"

    def categorize(self, prompt, threshold):
        categorized = categorize_prompt(prompt, threshold)
        result_text = format_categorized_prompt(categorized)
        return (result_text,)


NODE_CLASS_MAPPINGS = {
    "PromptCategorizer": PromptCategorizer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCategorizer": "🧠 Prompt Categorizer (Simple NLP)"
}
