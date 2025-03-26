import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import os
from collections import defaultdict

class DistilBertPromptClassifier:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "classify"
    CATEGORY = "🧠 Prompt Master"

    def __init__(self):
        base_dir = os.path.dirname(__file__)
        model_dir = os.path.join(base_dir, "distilbert_model")
        label_path = os.path.join(base_dir, "label_list.txt")

        self.tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_dir)
        self.model.eval()

        with open(label_path, "r", encoding="utf-8") as f:
            self.labels = [line.strip() for line in f.readlines()]

    def classify(self, text):
        tags = [tag.strip() for line in text.splitlines() for tag in line.split(",") if tag.strip()]
        categorized = defaultdict(list)

        for tag in tags:
            inputs = self.tokenizer(tag, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.softmax(outputs.logits, dim=1)
                label_idx = torch.argmax(probs, dim=1).item()
                confidence = probs[0, label_idx].item()

                label = self.labels[label_idx] if confidence > 0.6 else "기타"  # 60% 이상일 때만 인정
                categorized[label].append(tag)

        output_lines = []
        for label in self.labels + ["기타"]:  # 기타를 마지막에 추가
            if categorized[label]:
                output_lines.append(f"#{label}#")
                output_lines.append(", ".join(sorted(categorized[label])))
                output_lines.append("")

        return ("\n".join(output_lines),)
