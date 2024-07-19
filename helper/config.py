from enum import Enum


class Search(Enum):
    GOOGLE = 1
    TAVILY = 2

MODEL = "gpt-4o-mini"
SEARCH_ENGINE = Search.TAVILY
