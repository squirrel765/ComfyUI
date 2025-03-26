import re



class PromptTagFilter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_text": ("STRING", {
                    "multiline": True,
                    "default": "#퀄리티 프롬#\n(masterpiece, best quality), #기본 캐릭터 프롬#\n1girl, car"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filtered_text",)
    FUNCTION = "filter_tags"
    CATEGORY = "prompt_master/utils"

    def filter_tags(self, prompt_text):
        # 1. #으로 감싸진 부분 제거
        cleaned_text = re.sub(r'#.*?#', '', prompt_text)

        # 2. 남은 텍스트에서 , 기준으로 나눈 후 정리
        parts = [part.strip() for part in cleaned_text.split(',')]
        filtered = [part for part in parts if part]  # 빈 문자열 제거
        result = ', '.join(filtered)
        return (result,)
