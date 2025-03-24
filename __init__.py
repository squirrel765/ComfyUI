from .prompt_combiner import NODE_CLASS_MAPPINGS as COMBINER_MAPPINGS
from .dynamic_prompt_switch import NODE_CLASS_MAPPINGS as SWITCH_MAPPINGS


NODE_CLASS_MAPPINGS = {
    **COMBINER_MAPPINGS,
    **SWITCH_MAPPINGS,
 
}

__all__ = ["NODE_CLASS_MAPPINGS"]
