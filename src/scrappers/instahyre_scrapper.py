import httpx

from .base import BaseScrapper
from utils import write_json_async

class InstahyreScrapper(BaseScrapper):
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
            response = await self.get_instahyre_company_page(client, self.link)
            jobs = await self.find_all_jobs(client, response.get("jobs"))
            write_json_async("data.json", jobs)

    
    async def find_all_jobs(self, client, jobs):
        if jobs is None or len(jobs) == 0:
            return
        
        fetched_jobs = []
        for job in jobs:
            job_url = f"{InstahyreScrapper.base_url}{job.get('resource_uri')}"
            print(job_url)
            job_response = await self.get_request_to(client, job_url)
            fetched_jobs.append(job_response)
        
        return fetched_jobs


    async def get_instahyre_company_page(self, client, link):
        return await self.get_request_to(client, link)
    

    async def get_request_to(self, client, link):
        response = await client.get(link, headers=self.headers)
        return response.json()
        