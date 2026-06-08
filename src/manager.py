import os
from dotenv import load_dotenv
from scrappers import InstahyreScrapper, YCombinatorScrapper
import httpx
from httpx import ConnectError
from writer import AsyncJsonlWriter



load_dotenv()
BACKEND_BASE_URL = os.getenv("HIRINGLENS_BE_URL", "http://localhost:8000")
COMPANY_API = os.getenv("COMPANY_API", "/api/v1/company")
COMPANY_API_URL = BACKEND_BASE_URL + COMPANY_API


class ScrapperManager():

    def __init__(self):
        self.comps = [
            "https://www.ycombinator.com/companies/clipboard/jobs"
        ]
        self.icomps = [
            "https://www.instahyre.com/api/v1/employer_misc/employer_profile/anon_employer/53676?getVisibleJobs=true&limit=10",
            "https://www.instahyre.com/api/v1/employer_misc/employer_profile/anon_employer/4?getVisibleJobs=true&limit=20",
            "https://www.instahyre.com/api/v1/employer_misc/employer_profile/anon_employer/49340?getVisibleJobs=true&limit=20",
        ]
        self.writer = None
    

    def _fetch_companies(self, name:str):
        url = f"{COMPANY_API_URL}?platform={name}"
        print(url)
        try:
            response = httpx.get(url)
            print(response)
        except ConnectError as e:
            print(f" GOT CONNECTION ERROR : {e}")
        except Exception as e:
            print(e)

        return self.comps
    

    async def start(self):
        companies = self._fetch_companies("hello")
        for company in companies:
            scrapper = YCombinatorScrapper(company)
            jobs = await scrapper.fetch_jobs()
            for i, job in enumerate(jobs):
                await self.write_json(job)
                print(f"{i} job is written")
            
        await self.close_file()

    async def i_start(self):
        companies = self._fetch_companies("hello")
        for company in companies:
            scraper = InstahyreScrapper(company)
            jobs = await scraper.fetch_jobs()
            print("Type :", type(jobs))
            for i, job in enumerate(jobs):
                await self.write_json(job)
                print(f"{i} job is written")
        
        await self.close_file()
        

    async def write_json(self, data, name: str = "ycombinators"):
        if self.writer is None:
            self.writer = AsyncJsonlWriter("./data",name)
            await self.writer.start()
        
        await self.writer.write(data)

    async def close_file(self):
        await self.writer.close()

