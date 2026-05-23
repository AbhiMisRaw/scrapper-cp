import httpx
import asyncio

from bs4 import BeautifulSoup


async def scrape_job_market(link):
    # Enable http2=True to help bypass modern anti-bot setups
    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
    
    async with httpx.AsyncClient(limits=limits) as client:
        resp = await client.get(link)
        html_doc = await resp.aread()
        soup = BeautifulSoup(html_doc, 'html.parser')

        print(soup.prettify())
        res = soup.find_all(id='similar-jobs')
        print("====")
        print(res)

        # Step 1: Scrape the main aggregator platforms (Benefits from pooling)
        # aggregator_urls = ["https://unstop.com", "https://cutshort.io"]
        # tasks = [client.get(url) for url in aggregator_urls]
        # responses = await asyncio.gather(*tasks)
        
        # Step 2: Extract individual career pages from responses and queue them
        # (These will establish fresh connections, but HTTP/2 protects them from instant bans)


asyncio.run(scrape_job_market("https://www.instahyre.com/jobs-at-joveo/"))
