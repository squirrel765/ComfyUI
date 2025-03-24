import os
import csv
import json

class PromptPresetAndCategoryNode:
    CATEGORY = "Prompt/Presets"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "combine_prompts"

    preset_path = os.path.join(os.path.dirname(__file__), "presets/preset_data.json")
    category_path = os.path.join(os.path.dirname(__file__), "categories")
    categories = [
        "Viewpoint", "Background", "Pose", "Action", "Action2", "Clothing", "Top", "Bottom", "Underwear", "Dress", "Swimsuit" # 필요한 카테고리 확장 가능
    ]

    @classmethod
    def INPUT_TYPES(cls):
        # 프리셋 + previous 같은 줄에 표시되도록 위치 조정
        inputs = {
            "required": {
                "preset": ("STRING", {"default": "None"})
            },
            "optional": {
                "previous": ("STRING", {"default": ""})
            }
        }

        # 프리셋 옵션 지정 (드롭다운 유지)
        presets = cls._load_presets()
        inputs["required"]["preset"] = (["None"] + list(presets.keys()), {"default": "None"})

        # 카테고리별 드롭다운 입력 생성 (순서를 유지)
        for category in cls.categories:
            options = cls._load_csv(category)
            key = category.lower().replace(" ", "_")
            inputs["required"][key] = (options,)

        return inputs

    @classmethod
    def _load_presets(cls):
        if not os.path.exists(cls.preset_path):
            return {}
        with open(cls.preset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _load_csv(cls, category):
        file_path = os.path.join(cls.category_path, f"{category}.csv")
        if not os.path.exists(file_path):
            return ["None"]
        with open(file_path, "r", encoding="utf-8") as f:
            return ["None"] + [row[0] for row in csv.reader(f) if row]

    def combine_prompts(self, preset="None", previous="", **kwargs):
        previous = previous.strip() if previous else ""

        presets = self._load_presets()
        preset_prompt = presets.get(preset, "").strip() if preset != "None" else ""

        category_prompts = []
        for key in [cat.lower().replace(" ", "_") for cat in self.categories]:
            value = kwargs.get(key)
            if value and value != "None" and not value.startswith("──"):
                category_prompts.append(value.strip())

        # 쉼표 구분자 기준으로 연결
        parts = []
        if previous:
            parts.append(previous)
        if preset_prompt:
            parts.append(preset_prompt)
        if category_prompts:
            parts.extend(category_prompts)

        return (", ".join(parts),)


NODE_CLASS_MAPPINGS = {
    "Prompt Combiner": PromptPresetAndCategoryNode
}
