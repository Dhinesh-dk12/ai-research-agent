import re
from urllib.parse import urlparse, parse_qs, unquote


class ResultProcessor:
    """
    Process search results returned by Tavily MCP.
    Responsible for extracting, cleaning and ranking URLs.
    """

    URL_PATTERN = re.compile(
        r"https?://[^\s<>\"]+"
    )

    SKIP_EXTENSIONS = (
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".svg",
        ".ico",
        ".pdf",
        ".zip",
        ".css",
        ".js",
        ".woff",
        ".woff2",
        ".ttf",
        ".xml",
    )

    SKIP_DOMAINS = (
        "youtube.com",
        "youtu.be",
        "twitter.com",
        "x.com",
        "facebook.com",
        "instagram.com",
        "linkedin.com",
        "tiktok.com",
        "pinterest.com",
        "wiktionary.org",
        "tinyurl.com",
        "bit.ly",
        "goo.gl",
    )

    PRIORITY_KEYWORDS = (
        "docs",
        "documentation",
        "github",
        "blog",
        "guide",
        "tutorial",
        "learn",
        "research",
        "article",
    )

    @staticmethod
    def unwrap_translate(
        url: str,
    ) -> str:
        """
        Google Translate's proxy (translate.google.com/translate?u=...)
        wraps the real URL in a query parameter. Unwrap it so citations
        point at the original source instead of the translation proxy.
        """

        parsed = urlparse(url)

        host = parsed.hostname or ""

        if host == "translate.google.com" or host.endswith(
            ".translate.google.com"
        ):

            target = parse_qs(
                parsed.query
            ).get("u")

            if target:
                return unquote(target[0])

        return url

    @classmethod
    def extract_urls(
        cls,
        text: str,
    ) -> list[str]:

        urls = cls.URL_PATTERN.findall(
            text
        )

        cleaned_urls = []

        for url in urls:

            url = cls.clean_url(
                url
            )

            url = cls.unwrap_translate(
                url
            )

            if not url.startswith(
                (
                    "http://",
                    "https://",
                )
            ):
                continue

            if cls.should_skip(
                url
            ):
                continue

            cleaned_urls.append(
                url
            )

        # Remove duplicates
        cleaned_urls = list(
            dict.fromkeys(
                cleaned_urls
            )
        )

        # Rank URLs
        cleaned_urls.sort(
            key=cls.rank_url,
            reverse=True,
        )

        return cleaned_urls

    @staticmethod
    def clean_url(
        url: str,
    ) -> str:

        url = url.strip()

        url = url.rstrip(
            ").,;:]>}\"'"
        )

        url = re.sub(
            r"\[\d+\]$",
            "",
            url,
        )

        # Remove fragments
        url = url.split(
            "#"
        )[0]

        return url

    @classmethod
    def should_skip(
        cls,
        url: str,
    ) -> bool:

        lower = url.lower()

        host = urlparse(lower).hostname or ""

        # Skip social media and low-value domains
        for domain in cls.SKIP_DOMAINS:

            if host == domain or host.endswith(
                "." + domain
            ):
                return True

        # Skip Next.js image proxy URLs
        if "/_next/image" in lower:
            return True

        path = urlparse(lower).path

        # Skip common static assets
        for ext in cls.SKIP_EXTENSIONS:

            if path.endswith(ext):
                return True

        return False

    @classmethod
    def rank_url(
        cls,
        url: str,
    ) -> int:

        score = 0

        lower = url.lower()

        for keyword in cls.PRIORITY_KEYWORDS:

            if keyword in lower:
                score += 5

        if "github.com" in lower:
            score += 10

        if "docs." in lower:
            score += 8

        if "/docs/" in lower:
            score += 8

        if "medium.com" in lower:
            score += 4

        if "nature.com" in lower:
            score += 15

        if "arxiv.org" in lower:
            score += 15

        if "ieee.org" in lower:
            score += 15

        if "gov" in (
            urlparse(lower).hostname or ""
        ).split("."):
            score += 15

        if "edu" in (
            urlparse(lower).hostname or ""
        ).split("."):
            score += 15

        return score