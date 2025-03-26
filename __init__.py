from .prompt_combiner import NODE_CLASS_MAPPINGS as COMBINER_MAPPINGS
from .dynamic_prompt_switch import NODE_CLASS_MAPPINGS as SWITCH_MAPPINGS
from .filter_prompt_tags import PromptTagFilter
from .prompt_categorizer import NODE_CLASS_MAPPINGS as CATEGORIZER_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CATEGORIZER_DISPLAY
from .prompt_classifier import DistilBertPromptClassifier

NODE_CLASS_MAPPINGS = {
    **COMBINER_MAPPINGS,
    **SWITCH_MAPPINGS,
     "PromptTagFilter": PromptTagFilter,
     **CATEGORIZER_MAPPINGS,
      "DistilBertPromptClassifier": DistilBertPromptClassifier,
    
 
}

NODE_DISPLAY_NAME_MAPPINGS = {
     **CATEGORIZER_DISPLAY,
    "PromptTagFilter": "🧹 Filter #Hashed# Tags",
    "DistilBertPromptClassifier": "DistilBERT Prompt Classifier",
    
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
