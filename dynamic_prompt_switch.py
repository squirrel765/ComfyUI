class PromptSwitchHub:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_1": ("STRING", {"multiline": True}),
                "enabled_1": ("BOOLEAN", {"default": True}),
                "prompt_2": ("STRING", {"multiline": True}),
                "enabled_2": ("BOOLEAN", {"default": False}),
                "prompt_3": ("STRING", {"multiline": True}),
                "enabled_3": ("BOOLEAN", {"default": False}),
                "prompt_4": ("STRING", {"multiline": True}),
                "enabled_4": ("BOOLEAN", {"default": False}),
                "prompt_5": ("STRING", {"multiline": True}),
                "enabled_5": ("BOOLEAN", {"default": False}),
                "prompt_6": ("STRING", {"multiline": True}),
                "enabled_6": ("BOOLEAN", {"default": False}),
                "prompt_7": ("STRING", {"multiline": True}),
                "enabled_7": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "combine_active_prompts"
    CATEGORY = "Custom/Prompt"

    def combine_active_prompts(self,
                               prompt_1, enabled_1,
                               prompt_2, enabled_2,
                               prompt_3, enabled_3,
                               prompt_4, enabled_4,
                               prompt_5, enabled_5,
                               prompt_6, enabled_6,
                               prompt_7, enabled_7):
        result = []

        if enabled_1 and prompt_1.strip():
            result.append(prompt_1.strip())
        if enabled_2 and prompt_2.strip():
            result.append(prompt_2.strip())
        if enabled_3 and prompt_3.strip():
            result.append(prompt_3.strip())
        if enabled_4 and prompt_4.strip():
            result.append(prompt_4.strip())
        if enabled_5 and prompt_5.strip():
            result.append(prompt_5.strip())
        if enabled_6 and prompt_6.strip():
            result.append(prompt_6.strip())
        if enabled_7 and prompt_7.strip():
            result.append(prompt_7.strip())

        return (", ".join(result),)


NODE_CLASS_MAPPINGS = {
    "PromptSwitchHub": PromptSwitchHub
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptSwitchHub": "Prompt Switch Hub"
}
