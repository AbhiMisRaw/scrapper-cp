import httpx

from .base import BaseScrapper
from utils import write_json_async
from writer.jsonl_writer import AsyncJsonlWriter

class InstahyreScrapper(BaseScrapper):
    name = "instahyre"
    base_url = "https://www.instahyre.com"

    def __init__(self, link: str):
        self.link = link
        self.headers = {
            "User-Agent": (
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }


    async def fetch_jobs(self):
        """
        Instance method to fetch a company's all job in a single TCP connection.
        """
        
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        async with httpx.AsyncClient(limits=limits) as client:
            # Step 1: Scrape the main aggregator platforms (Benefits from pooling)
            response = await self._get_instahyre_company_page(client, self.link)
            jobs = await self._find_all_jobs(client, response.get("jobs"))
            return jobs            

    
    async def _find_all_jobs(self, client, jobs):
        if jobs is None or len(jobs) == 0:
            return
        
        fetched_jobs = []
        for job in jobs:
            job_url = f"{InstahyreScrapper.base_url}{job.get('resource_uri')}"
            print(job_url)
            job_response = await self._get_request_to(client, job_url)
            fetched_jobs.append(job_response)
        
        return fetched_jobs


    async def _get_instahyre_company_page(self, client, link):
        return await self._get_request_to(client, link)
    

    async def _get_request_to(self, client, link):
        response = await client.get(link, headers=self.headers)
        return response.json()
        