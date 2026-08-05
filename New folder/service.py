import asyncio
import os
from summarizer.service import (
    SummarizerService
)
from executor.service import ExecutorService
from executor.result_processor import ResultProcessor
from report.pdf_service import PDFService
from research.collector import EvidenceCollector
from research.evidence import Evidence

from reasoning.service import ReasoningService
from report.service import ReportService

from extractor.scrapling_extractor import ScraplingExtractor

from memory.service import MemoryService

from utils.logger import logger


class ResearchService:

    def __init__(self):

        self.executor = ExecutorService()

        self.collector = EvidenceCollector()
        self.summarizer = (
    SummarizerService()
)

        self.reasoning = ReasoningService()

        self.reporter = ReportService()

        self.extractor = ScraplingExtractor()
        self.pdf_service = PDFService()

        self.memory = MemoryService()

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

    async def run(
        self,
        state,
    ):

        logger.info(
            "Starting research workflow"
        )

        # --------------------------------------------------
        # Execute Search Tasks
        # --------------------------------------------------

        state = await self.executor.execute(
            state
        )

        logger.info(
            "Processing search results..."
        )

        urls = []

        for result in state.task_results.values():

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

        # --------------------------------------------------
        # Parallel Extraction
        # --------------------------------------------------

        MAX_URLS = 10

        logger.info(
            f"Starting parallel extraction for top {MAX_URLS} URLs"
        )

        semaphore = asyncio.Semaphore(
            5
        )

        tasks = [

            self.process_url(
                url,
                semaphore,
            )

            for url in urls[:MAX_URLS]

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
            f"Collected {len(self.collector.get_all())} evidence documents"
        )

        # --------------------------------------------------
        # Retrieve Related Memories
        # --------------------------------------------------

        logger.info(
            "Retrieving related memories..."
        )

        try:

            memory_results = self.memory.retrieve(
                query=state.query,
                top_k=5,
            )

            documents = memory_results.get(
                "documents",
                []
            )

            metadatas = memory_results.get(
                "metadatas",
                []
            )

            if (

                documents

                and len(documents) > 0

                and len(documents[0]) > 0

            ):

                logger.info(
                    f"Found {len(documents[0])} related memories"
                )

                for document, metadata in zip(

                    documents[0],

                    metadatas[0],

                ):

                    evidence = Evidence(

                        source_url=metadata.get(
                            "source_url",
                            "memory",
                        ),

                        content=document,
                    )

                    self.collector.add_evidence(
                        evidence
                    )

                logger.success(
                    "Previous memories merged into evidence."
                )

            else:

                logger.info(
                    "No related memories found."
                )

        except Exception as e:

            logger.warning(
                f"Memory retrieval failed: {e}"
            )

        logger.info(
            f"Total evidences available: {len(self.collector.get_all())}"
        )

        # --------------------------------------------------
        # Reasoning
        # --------------------------------------------------

        logger.info(
            "Starting reasoning..."
        )

        reasoning_output = (

            await self.reasoning.analyze(

                query=state.query,

                evidences=self.collector.get_all(),

            )

        )

        logger.success(
            "Reasoning completed"
        )

        # --------------------------------------------------
        # Store Fresh Memories
        # --------------------------------------------------

        logger.info(
            "Saving fresh evidences into memory..."
        )

        stored = 0

        for evidence in fresh_evidences:

            try:

                self.memory.store_memory(

                    query=state.query,

                    source_url=evidence.source_url,

                    content=evidence.content,

                )

                stored += 1

            except Exception as e:

                logger.warning(
                    f"Failed storing memory: {e}"
                )

        logger.success(
            f"{stored} evidences stored."
        )

        # --------------------------------------------------
        # Report Generation
        # --------------------------------------------------

        logger.info(
            "Generating final report..."
        )

        report = (

            await self.reporter.generate_report(

                query=state.query,

                reasoning_output=reasoning_output,

            )

        )

        os.makedirs(
            "reports",
            exist_ok=True,
        )

        pdf_path = (
            "reports/final_report.pdf"
        )
        self.pdf_service.generate_pdf(
            markdown_text=report,
            output_path=pdf_path,
        )

        

        logger.success(
            f"Research Report Saved as PDF to {pdf_path}"
        )

        logger.success(
            "Research workflow completed successfully."
        )

        return report