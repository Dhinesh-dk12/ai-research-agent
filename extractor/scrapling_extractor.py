from scrapling import Fetcher

from utils.logger import logger


class ScraplingExtractor:

    def __init__(self):

        self.fetcher = Fetcher()

    async def extract(
        self,
        url: str,
    ) -> str:

        logger.info(
            f"Downloading page: {url}"
        )

        try:

            page = self.fetcher.get(
                url,
                timeout=30,
            )

        except Exception as e:

            logger.exception(
                f"Failed downloading {url}: {e}"
            )

            return ""

        if page is None:

            logger.warning(
                f"No page returned: {url}"
            )

            return ""

        try:

            content = page.get_all_text()

        except Exception as e:

            logger.exception(
                f"Failed extracting text from {url}: {e}"
            )

            return ""

        if not content:

            logger.warning(
                f"No readable content found: {url}"
            )

            return ""

        logger.info(
            f"Extracted {len(content)} characters"
        )

        return content