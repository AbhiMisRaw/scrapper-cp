
from scrappers import InstahyreScrapper
from writer import AsyncJsonlWriter

class ScrapperManager():

    def __init__(self):
        self.comps = [
            "https://www.instahyre.com/api/v1/employer_misc/employer_profile/anon_employer/53676?getVisibleJobs=true&limit=10",
            "https://www.instahyre.com/api/v1/employer_misc/employer_profile/anon_employer/4?getVisibleJobs=true&limit=20",
            "https://www.instahyre.com/api/v1/employer_misc/employer_profile/anon_employer/49340?getVisibleJobs=true&limit=20",
        ]
        self.writer = None
    

    def _fetch_companies(self, name:str):
        return self.comps


    async def start(self):
        companies = self._fetch_companies("hello")
        for company in companies:
            scraper = InstahyreScrapper(company)
            jobs = await scraper.fetch_jobs()
            print("Type :", type(jobs))
            for i, job in enumerate(jobs):
                await self.write_json(job)
                print(f"{i} job is written")
        
        await self.close_file()
        

    async def write_json(self, data, name: str = "instahyre"):
        if self.writer is None:
            self.writer = AsyncJsonlWriter("./data",name)
            await self.writer.start()
        
        await self.writer.write(data)

    async def close_file(self):
        await self.writer.close()

