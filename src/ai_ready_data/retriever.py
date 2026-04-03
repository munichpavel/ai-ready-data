from pathlib import Path
from typing import Callable

Retriever = Callable[[str], str]


def null_retriever(query: str) -> str:
    return ""


def make_full_context_retriever(parsed_dir: Path) -> Retriever:
    def retrieve(query: str) -> str:
        docs = []
        docs += [p.read_text() for p in parsed_dir.glob("*.txt")]
        docs += [p.read_text() for p in parsed_dir.glob("*.csv")]
        return "\n\n".join(docs)
    return retrieve
