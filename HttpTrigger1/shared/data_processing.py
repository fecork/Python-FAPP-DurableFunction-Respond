"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.1
"""
import re
from typing import Dict


def format_text(text: str) -> str:
    """Preprocesses the data text, clean it.

    Args:
        text: String Raw data.
    Returns:
        Preprocessed data text, without stranger character.
    """

    text = text.replace(str("\\n"), "\n")
    text = text.replace(str("/"), " ")
    text = re.sub(r"[^a-zA-Z0-9\s\n.,;]", "", text)
    return text