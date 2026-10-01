from dataclasses import dataclass
from urllib.parse import urlparse


# ----------------------------------------------------------------
# Domain-based source credibility.
#
# This is a simple, transparent heuristic based on WHO published the
# page. It is not a fact-check: a high score means "generally reliable
# publisher", not "every claim is correct". Add or remove domains here
# to match your own judgement.
# ----------------------------------------------------------------

_DOMAIN_TIERS = [

    (
        90,
        "official / intergovernmental body",
        (
            "rbi.org.in",
            "nseindia.com",
            "bseindia.com",
            "nic.in",
            "worldbank.org",
            "imf.org",
            "oecd.org",
            "un.org",
            "who.int",
            "europa.eu",
            "bis.org",
            "wto.org",
            "ifr.org",
        ),
    ),

    (
        90,
        "academic / peer-reviewed publisher",
        (
            "arxiv.org",
            "nature.com",
            "science.org",
            "sciencedirect.com",
            "springer.com",
            "ieee.org",
            "acm.org",
            "jstor.org",
            "pnas.org",
            "cell.com",
        ),
    ),

    (
        75,
        "major news outlet",
        (
            "reuters.com",
            "bloomberg.com",
            "ft.com",
            "wsj.com",
            "bbc.com",
            "bbc.co.uk",
            "cnbc.com",
            "economist.com",
            "nytimes.com",
            "apnews.com",
            "theguardian.com",
            "livemint.com",
            "economictimes.indiatimes.com",
            "thehindu.com",
            "business-standard.com",
            "moneycontrol.com",
        ),
    ),

    (
        75,
        "research / consulting firm",
        (
            "mckinsey.com",
            "bain.com",
            "bcg.com",
            "deloitte.com",
            "pwc.com",
            "kpmg.com",
            "ey.com",
            "gartner.com",
            "forrester.com",
            "idc.com",
        ),
    ),

    (
        65,
        "market data aggregator",
        (
            "tradingeconomics.com",
            "screener.in",
            "trendlyne.com",
            "investing.com",
            "tradingview.com",
            "statista.com",
            "macrotrends.net",
        ),
    ),

    (
        60,
        "encyclopedia (secondary source)",
        (
            "wikipedia.org",
            "britannica.com",
        ),
    ),

    (
        30,
        "blog / user-generated / crypto news",
        (
            "medium.com",
            "blogspot.com",
            "wordpress.com",
            "substack.com",
            "quora.com",
            "reddit.com",
            "cryptorank.io",
            "cryptonews.com",
            "cointelegraph.com",
        ),
    ),

]

DEFAULT_SCORE = 50

# Hard cap on how much text one source may contribute to the prompt,
# so no single page can dominate the analysis.
MAX_CHARS_PER_SOURCE = 6000


@dataclass(frozen=True)
class Credibility:

    score: int

    label: str


@dataclass(frozen=True)
class Source:
    """
    One unique URL with all of its evidence merged together.
    """

    source_url: str

    content: str

    credibility: Credibility


def score_source(url: str) -> Credibility:

    host = (urlparse(url).hostname or "").lower()

    if host.startswith("www."):
        host = host[4:]

    if not host:
        return Credibility(40, "unknown source")

    for score, label, domains in _DOMAIN_TIERS:

        for domain in domains:

            if host == domain or host.endswith("." + domain):

                return Credibility(score, label)

    labels = host.split(".")

    if "gov" in labels:
        return Credibility(90, "government website")

    if "edu" in labels or (
        len(labels) >= 2 and labels[-2] == "ac"
    ):
        return Credibility(85, "academic institution")

    if host.startswith("blog."):
        return Credibility(35, "company / personal blog")

    return Credibility(DEFAULT_SCORE, "general website")


def group_evidences(evidences) -> list[Source]:
    """
    Merge evidence that shares a URL into one source (so each URL gets
    exactly one citation number), cap the text per source, and order
    sources from most to least credible.
    """

    grouped: dict[str, list[str]] = {}

    for evidence in evidences:

        contents = grouped.setdefault(
            evidence.source_url,
            [],
        )

        if evidence.content not in contents:
            contents.append(evidence.content)

    sources = []

    for url, contents in grouped.items():

        text = "\n\n".join(contents)

        if len(text) > MAX_CHARS_PER_SOURCE:
            text = text[:MAX_CHARS_PER_SOURCE] + " ..."

        sources.append(
            Source(
                source_url=url,
                content=text,
                credibility=score_source(url),
            )
        )

    # sort() is stable, so equally credible sources keep their order
    sources.sort(
        key=lambda source: source.credibility.score,
        reverse=True,
    )

    return sources