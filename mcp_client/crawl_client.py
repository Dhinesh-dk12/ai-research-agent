from crawl4ai import AsyncWebCrawler


class CrawlClient:

    async def crawl(self, url: str) -> str:
        """
        Crawl a webpage and return clean markdown.
        """

        async with AsyncWebCrawler() as crawler:

            result = await crawler.arun(
                url=url
            )

            return result.markdown