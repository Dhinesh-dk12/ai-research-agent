import asyncio

from executor.result_processor import (
    ResultProcessor,
)

from extractor.scrapling_extractor import (
    ScraplingExtractor,
)

from summarizer.service import (
    SummarizerService,
)

from research.collector import (
    EvidenceCollector,
)

from research.evidence import (
    Evidence,
)

from utils.logger import (
    logger,
)


class ExtractionService:

    def __init__(self):

        self.extractor = (
            ScraplingExtractor()
        )

        self.summarizer = (
            SummarizerService()
        )

        self.collector = (
            EvidenceCollector()
        )

    async def process_url(

        self,

        url: str,

        semaphore: asyncio.Semaphore,

    ):

        async with semaphore:

            logger.info(
                f"Extracting: {url}"
            )

            try:

                content = await self.extractor.extract(
                    url
                )

                if not content:

                    logger.warning(
                        f"No content extracted from {url}"
                    )

                    return None

                if len(
                    content.strip()
                ) < 300:

                    logger.warning(
                        f"Skipping short page: {url}"
                    )

                    return None

                logger.info(
                    f"Extracted {len(content)} characters"
                )

                summary = await self.summarizer.summarize(
                    content
                )

                logger.info(
                    f"Summary size: {len(summary)}"
                )

                return Evidence(

                    source_url=url,

                    content=summary,

                )

            except Exception as e:

                logger.exception(
                    f"Failed to extract {url}: {e}"
                )

                return None

    async def extract(

        self,

        task_results: dict,

        max_urls: int = 10,

        concurrency: int = 5,

    ):

        logger.info(
            "Processing search results..."
        )

        urls = []

        for result in task_results.values():

            try:

                text = result.content[0].text

                extracted_urls = (
                    ResultProcessor.extract_urls(
                        text
                    )
                )

                urls.extend(
                    extracted_urls
                )

            except Exception as e:

                logger.warning(
                    f"Failed to process search result: {e}"
                )

        urls = list(
            dict.fromkeys(urls)
        )

        logger.info(
            f"Found {len(urls)} clean URLs"
        )

        logger.info(
            f"Starting parallel extraction for top {max_urls} URLs"
        )

        semaphore = asyncio.Semaphore(
            concurrency
        )

        tasks = [

            self.process_url(
                url,
                semaphore,
            )

            for url in urls[:max_urls]

        ]

        results = await asyncio.gather(

            *tasks,

            return_exceptions=True,

        )

        fresh_evidences = []

        for result in results:

            if isinstance(
                result,
                Evidence,
            ):

                self.collector.add_evidence(
                    result
                )

                fresh_evidences.append(
                    result
                )

        logger.success(
            "Parallel extraction completed."
        )

        logger.info(
            f"Collected {len(fresh_evidences)} evidence documents"
        )

        return (

            urls,

            fresh_evidences,

        )