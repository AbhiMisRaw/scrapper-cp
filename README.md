## Scrapper Service

This is Scrapper Service.

### Tech Stack :

- Python
- HTTPX
- BeautifulSoup
- MiniIO

### Flow

1. Scrapper Service fetches company list.
```
Scrapper Service --> GET HTTP -> CrowdPulse API
Scrapper Service <-- Companies List <-- CrowdPulse API 
```

2. Scrapper Service fetches One company career jobs from each platform
```
SS -> GET HTTP --> Platform APIs
SS <-- Job Description <-- Platform APIs
```

3. Scrapper Service saves these jobs to MiniIO.
```
SS --> POST JobDescription Data --> MiniIO
```