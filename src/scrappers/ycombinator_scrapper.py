import httpx

from .base import BaseScrapper


class YCombinatorScrapper(BaseScrapper):
    name = "ycombinator"
    base_url = "https://www.ycombinator.com/"

    def __init__(self, link: str):
        self.link = link
        self.headers = {
            "User-Agent": (
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }

