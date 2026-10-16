import asyncio

from scrapling import Fetcher, StealthyFetcher

from utils.logger import logger


# Matches the "skip short page" threshold in extraction_service.py.
# Below this, the plain fetcher likely got a bot-check stub instead
# of the real page (seen repeatedly with pmc.ncbi.nlm.nih.gov, which
# returns an identical ~150-character stub to non-browser clients).
MIN_CONTENT_LENGTH = 300


class ScraplingExtractor:

    def __init__(self):

        self.fetcher = Fetcher()

    async def _fetch_plain(
        self,
        url: str,
    ) -> str:

        try:

            page = await asyncio.to_thread(
                self.fetcher.get,
                url,
                timeout=30,
            )

        except Exception as e:

            logger.warning(
                f"Plain fetch failed for {url}: {e}"
            )

            return ""

        if page is None:

            return ""

        try:

            return await asyncio.to_thread(
                page.get_all_text
            )

        except Exception as e:

            logger.warning(
                f"Failed extracting text from {url}: {e}"
            )

            return ""

    async def _fetch_stealthy(
        self,
        url: str,
    ) -> str:
        """
        Fallback for pages that return a bot-check stub (or nothing)
        to the plain fetcher. Uses a real headless browser via
        Scrapling's StealthyFetcher, so it's slower but can get past
        basic bot detection that blocks the plain HTTP fetcher.
        """

        try:

            page = await StealthyFetcher.async_fetch(

                url,

                timeout=30000,  # this fetcher takes milliseconds

                network_idle=True,

            )

        except Exception as e:

            logger.warning(
                f"Stealthy fetch failed for {url}: {e}"
            )

            return ""

        if page is None:

            return ""

        try:

            return page.get_all_text()

        except Exception as e:

            logger.warning(
                f"Failed extracting stealthy text from {url}: {e}"
            )

            return ""

    async def extract(
        self,
        url: str,
    ) -> str:

        logger.info(
            f"Downloading page: {url}"
        )

        content = await self._fetch_plain(
            url
        )

        if content and len(
            content.strip()
        ) >= MIN_CONTENT_LENGTH:

            logger.info(
                f"Extracted {len(content)} characters"
            )

            return content

        logger.info(
            f"Plain fetch too short "
            f"({len(content.strip()) if content else 0} chars) "
            f"for {url}, retrying with stealthy browser fetcher"
        )

        stealthy_content = await self._fetch_stealthy(
            url
        )

        if stealthy_content and len(
            stealthy_content.strip()
        ) >= MIN_CONTENT_LENGTH:

            logger.info(
                f"Stealthy fetch extracted "
                f"{len(stealthy_content)} characters"
            )

            return stealthy_content

        logger.warning(
            f"No readable content found (both fetchers): {url}"
        )

        # Return whatever's longer; extraction_service still applies
        # its own short-page check on the result.
        return (
            stealthy_content
            if len(stealthy_content or "") > len(content or "")
            else content
        ) or ""
