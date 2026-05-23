import asyncio
import httpx

from .base import BaseScrapper

class InstahyreScrapper(BaseScrapper):

    def __init__(self, base_link: str):
        self.link = base_link


    async def fetch_jobs(self):
        # Enable http2=True to help bypass modern anti-bot setups
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        
        async with httpx.AsyncClient(limits=limits) as client:
            # Step 1: Scrape the main aggregator platforms (Benefits from pooling)
            
            aggregator_urls = []
            tasks = [client.get(url) for url in aggregator_urls]
            responses = await asyncio.gather(*tasks)
            
            # Step 2: Extract individual career pages from responses and queue them
            # (These will establish fresh connections, but HTTP/2 protects them from instant bans)