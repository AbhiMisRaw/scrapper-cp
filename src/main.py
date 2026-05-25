import httpx
import asyncio
import pprint
from copy import deepcopy

from utils import write_json_async

INSTAHYRE_BASE_URL = "https://www.instahyre.com"

async def scrape_job_market(link):
    # Enable http2=True to help bypass modern anti-bot setups
    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
    
    async with httpx.AsyncClient(limits=limits) as client:
        headers = {
            "User-Agent": (
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }
        response = await client.get(link, headers=headers)
        resp = response.json()
        fetched_jobs = []
        for job in resp.get("jobs"):
            job_url = f"{INSTAHYRE_BASE_URL}{job.get('resource_uri')}"
            print(job_url)
            job_response = await client.get(job_url, headers=headers)
            job_overview = job_response.json()
            fetched_jobs.append(job_overview)

        jobs = deepcopy(resp.get("jobs"))
        print("jobs in this company.")
        
        await write_json_async("data_v1.json",fetched_jobs)


asyncio.run(scrape_job_market("https://www.instahyre.com/api/v1/employer_misc/employer_profile/anon_employer/53676?getVisibleJobs=true&limit=10"))
