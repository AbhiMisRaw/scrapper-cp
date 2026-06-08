import httpx
from bs4 import BeautifulSoup
from .base import BaseScrapper


class YCombinatorScrapper(BaseScrapper):
    name = "ycombinator"
    base_url = "https://www.ycombinator.com"

    def __init__(self, link: str):
        self.link = link
        self.headers = {
            "User-Agent": (
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }

    async def fetch_jobs(self):
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        async with httpx.AsyncClient(limits=limits) as client:
            response = await client.get(self.link)
            import pprint
            if response.status_code != 200:
                return None
            
            jobs = self._collect_jobs(response)
            pprint.pprint(jobs)
            data = list()
            
            for job in jobs:
                response = await client.get(f"{self.base_url}/{job.get("url")}")
                info = self._extract_info(response)
                pprint.pprint(info)
                data.append(info)
        

            return data
    

    def _collect_jobs(self, docuemnt):
        tree = BeautifulSoup(docuemnt, "html.parser")

        jobs = []
        for title_div in tree.select("div.ycdc-with-link-color"):
            a = title_div.find("a", href=True)

            if not a:
                continue

            jobs.append({
                "title": a.get_text(strip=True),
                "url": a["href"]
            })

        return jobs


    def _extract_info(self, document):
        soup = BeautifulSoup(document, "html.parser")

        job = {}

        card = soup.select_one("div.ycdc-card")

        if not card:
            return {}

        # title
        title = card.select_one("h1")
        if title:
            job["title"] = title.get_text(strip=True)

        # location
        location_div = card.select_one(
            "div.flex.flex-wrap.items-center.text-base"
        )

        if location_div:
            spans = location_div.find_all("span")

            if spans:
                job["location"] = spans[-1].get_text(strip=True)

        # metadata
        metadata = card.select_one(
            "div.mt-5.flex.flex-wrap.gap-x-6.gap-y-3.text-sm"
        )

        if metadata:

            for field in metadata.find_all("div", recursive=False):

                label = field.find("strong")
                value = field.find("span")

                if not label or not value:
                    continue

                key = (
                    label.get_text(strip=True)
                    .lower()
                    .replace(" ", "_")
                )

                job[key] = value.get_text(strip=True)

        return job

