import os
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ----------------------------------------------------------------
# Fonts
#
# ReportLab's built-in fonts miss many characters (for example the
# rupee sign, arrows, math symbols). We try to use a TrueType font
# installed on the system and fall back to Helvetica if none is found.
# Each entry is (regular, bold, italic, bold-italic).
# ----------------------------------------------------------------

_FONT_CANDIDATES = [
    (
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeuii.ttf",
        "C:/Windows/Fonts/segoeuiz.ttf",
    ),
    (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/ariali.ttf",
        "C:/Windows/Fonts/arialbi.ttf",
    ),
    (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
    ),
]


def _register_fonts() -> tuple[str, str]:
    """
    Returns (regular_font_name, bold_font_name).
    """

    for index, paths in enumerate(_FONT_CANDIDATES):

        if not all(os.path.exists(path) for path in paths):
            continue

        try:

            family = f"ReportFont{index}"

            names = [
                f"{family}-Regular",
                f"{family}-Bold",
                f"{family}-Italic",
                f"{family}-BoldItalic",
            ]

            for name, path in zip(names, paths):

                pdfmetrics.registerFont(
                    TTFont(name, path)
                )

            pdfmetrics.registerFontFamily(
                family,
                normal=names[0],
                bold=names[1],
                italic=names[2],
                boldItalic=names[3],
            )

            # registerFontFamily lower-cases the family key, and the
            # regular font name is what styles must use.
            pdfmetrics.registerFontFamily(
                names[0],
                normal=names[0],
                bold=names[1],
                italic=names[2],
                boldItalic=names[3],
            )

            return names[0], names[1]

        except Exception:
            continue

    return "Helvetica", "Helvetica-Bold"


# ----------------------------------------------------------------
# Markdown patterns
# ----------------------------------------------------------------

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")

_HR = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})$")

_BULLET = re.compile(r"^(\s*)[-*+]\s+(.*)$")

_NUMBERED = re.compile(r"^\s*(\d+)[.)]\s+(.*)$")

_QUOTE = re.compile(r"^>\s?(.*)$")

_TABLE_SEPARATOR_CELL = re.compile(r"^\s*:?-+:?\s*$")

_CODE = re.compile(r"`([^`]+)`")

_BOLD = re.compile(r"\*\*(.+?)\*\*")

_ITALIC = re.compile(
    r"(?<![\*\w])\*(?![\s\*])(.+?)(?<![\s\*])\*(?![\*\w])"
)

_URL = re.compile(r"https?://[^\s<>()\"']+")


def _link(match: re.Match) -> str:

    url = match.group(0)

    trailing = ""

    while url and url[-1] in ".,;:!?":

        trailing = url[-1] + trailing

        url = url[:-1]

    return (
        f'<a href="{url}" color="#1a5fb4">{url}</a>'
        f"{trailing}"
    )


def _inline(raw: str) -> str:
    """
    Escape text for ReportLab and convert inline markdown
    (code, bold, italic, links) into ReportLab markup.
    """

    text = escape(raw)

    text = _CODE.sub(
        r'<font face="Courier">\1</font>',
        text,
    )

    text = _BOLD.sub(r"<b>\1</b>", text)

    text = _ITALIC.sub(r"<i>\1</i>", text)

    text = _URL.sub(_link, text)

    return text


def _split_row(line: str) -> list[str]:

    line = line.strip()

    if line.startswith("|"):
        line = line[1:]

    if line.endswith("|"):
        line = line[:-1]

    return [cell.strip() for cell in line.split("|")]


def _is_separator(line: str) -> bool:

    cells = _split_row(line)

    return bool(cells) and all(
        _TABLE_SEPARATOR_CELL.match(cell)
        for cell in cells
    )


class PDFService:
    """
    Converts the markdown report into a formatted PDF.

    Supports headings, paragraphs, bold / italic / inline code,
    clickable links, bullet and numbered lists (with nesting),
    tables, block quotes, code blocks and horizontal rules.
    """

    # ------------------------------------------------------------
    # Styles
    # ------------------------------------------------------------

    def _build_styles(
        self,
        font: str,
        bold: str,
    ) -> dict:

        base = getSampleStyleSheet()

        body = ParagraphStyle(
            "ReportBody",
            parent=base["BodyText"],
            fontName=font,
            fontSize=10,
            leading=14,
            spaceAfter=3,
        )

        return {

            "font": font,

            "body": body,

            "h1": ParagraphStyle(
                "ReportH1",
                parent=base["Heading1"],
                fontName=bold,
                fontSize=20,
                leading=25,
                alignment=TA_CENTER,
                spaceAfter=10,
            ),

            "h2": ParagraphStyle(
                "ReportH2",
                parent=base["Heading2"],
                fontName=bold,
                fontSize=15,
                leading=19,
                spaceBefore=12,
                spaceAfter=6,
            ),

            "h3": ParagraphStyle(
                "ReportH3",
                parent=base["Heading3"],
                fontName=bold,
                fontSize=12.5,
                leading=16,
                spaceBefore=8,
                spaceAfter=4,
            ),

            "h4": ParagraphStyle(
                "ReportH4",
                parent=body,
                fontName=bold,
                fontSize=10.5,
                spaceBefore=6,
            ),

            "quote": ParagraphStyle(
                "ReportQuote",
                parent=body,
                leftIndent=14,
                textColor=colors.HexColor("#444444"),
            ),

            "code": ParagraphStyle(
                "ReportCode",
                parent=body,
                fontName="Courier",
                fontSize=8.5,
                leading=11,
                leftIndent=8,
            ),

            "cell": ParagraphStyle(
                "ReportCell",
                parent=body,
                fontSize=9,
                leading=12,
                spaceAfter=0,
            ),

            "cell_head": ParagraphStyle(
                "ReportCellHead",
                parent=body,
                fontName=bold,
                fontSize=9,
                leading=12,
                spaceAfter=0,
            ),

            "list_cache": {},

        }

    def _list_style(
        self,
        styles: dict,
        level: int,
        numbered: bool,
    ) -> ParagraphStyle:

        key = (level, numbered)

        cache = styles["list_cache"]

        if key not in cache:

            cache[key] = ParagraphStyle(
                f"ReportList{level}{int(numbered)}",
                parent=styles["body"],
                leftIndent=(22 if numbered else 16) + 14 * level,
                bulletIndent=(4 if numbered else 4) + 14 * level,
                bulletFontName=styles["font"],
                spaceAfter=2,
            )

        return cache[key]

    # ------------------------------------------------------------
    # Building blocks
    # ------------------------------------------------------------

    @staticmethod
    def _para(
        raw: str,
        style: ParagraphStyle,
        bullet: str | None = None,
    ) -> Paragraph:

        try:

            return Paragraph(
                _inline(raw),
                style,
                bulletText=bullet,
            )

        except Exception:

            # Badly nested markup: fall back to plain escaped text
            # instead of failing the whole PDF.
            return Paragraph(
                escape(raw),
                style,
                bulletText=bullet,
            )

    def _table(
        self,
        rows: list[list[str]],
        width: float,
        styles: dict,
    ) -> Table:

        columns = max(len(row) for row in rows)

        rows = [
            row + [""] * (columns - len(row))
            for row in rows
        ]

        # Column widths proportional to the longest text in each column.
        lengths = [
            max(
                8,
                min(
                    60,
                    max(len(row[column]) for row in rows),
                ),
            )
            for column in range(columns)
        ]

        total = sum(lengths)

        column_widths = [
            width * length / total
            for length in lengths
        ]

        data = []

        for index, row in enumerate(rows):

            style = (
                styles["cell_head"]
                if index == 0
                else styles["cell"]
            )

            data.append(
                [self._para(cell, style) for cell in row]
            )

        table = Table(
            data,
            colWidths=column_widths,
            repeatRows=1,
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#E8ECF1"),
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#B0B7C3"),
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )

        return table

    @staticmethod
    def _find_title(markdown_text: str) -> str:

        for line in markdown_text.splitlines():

            match = re.match(r"^#\s+(.*)$", line.strip())

            if match:

                return re.sub(r"[*`]", "", match.group(1))

        return "Research Report"

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------

    def generate_pdf(
        self,
        markdown_text: str,
        output_path: str,
    ):

        font, bold = _register_fonts()

        styles = self._build_styles(font, bold)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54,
            title=self._find_title(markdown_text),
        )

        elements = []

        lines = markdown_text.splitlines()

        in_code = False

        index = 0

        while index < len(lines):

            raw = lines[index]

            stripped = raw.strip()

            # ---------------- code blocks ----------------

            if stripped.startswith("```"):

                in_code = not in_code

                index += 1

                continue

            if in_code:

                elements.append(
                    Preformatted(raw or " ", styles["code"])
                )

                index += 1

                continue

            # ---------------- blank line ----------------

            if not stripped:

                elements.append(Spacer(1, 6))

                index += 1

                continue

            # ---------------- horizontal rule ----------------

            if _HR.match(stripped):

                elements.append(
                    HRFlowable(
                        width="100%",
                        thickness=0.6,
                        color=colors.HexColor("#B0B7C3"),
                        spaceBefore=6,
                        spaceAfter=6,
                    )
                )

                index += 1

                continue

            # ---------------- headings ----------------

            heading = _HEADING.match(stripped)

            if heading:

                level = len(heading.group(1))

                style = styles[
                    "h1" if level == 1
                    else "h2" if level == 2
                    else "h3" if level == 3
                    else "h4"
                ]

                elements.append(
                    self._para(heading.group(2), style)
                )

                index += 1

                continue

            # ---------------- tables ----------------

            if stripped.startswith("|"):

                block = []

                end = index

                while (
                    end < len(lines)
                    and lines[end].strip().startswith("|")
                ):

                    block.append(lines[end].strip())

                    end += 1

                if len(block) >= 2 and _is_separator(block[1]):

                    rows = [_split_row(block[0])] + [
                        _split_row(line)
                        for line in block[2:]
                    ]

                    elements.append(
                        self._table(rows, doc.width, styles)
                    )

                    elements.append(Spacer(1, 8))

                    index = end

                    continue

            # ---------------- bullet lists ----------------

            bullet = _BULLET.match(raw)

            if bullet:

                spaces = len(bullet.group(1).expandtabs(4))

                level = (
                    0
                    if spaces == 0
                    else min(1 + (spaces - 1) // 4, 3)
                )

                elements.append(
                    self._para(
                        bullet.group(2),
                        self._list_style(styles, level, False),
                        bullet="•" if level == 0 else "–",
                    )
                )

                index += 1

                continue

            # ---------------- numbered lists ----------------

            numbered = _NUMBERED.match(raw)

            if numbered:

                elements.append(
                    self._para(
                        numbered.group(2),
                        self._list_style(styles, 0, True),
                        bullet=f"{numbered.group(1)}.",
                    )
                )

                index += 1

                continue

            # ---------------- block quotes ----------------

            quote = _QUOTE.match(stripped)

            if quote:

                elements.append(
                    self._para(quote.group(1), styles["quote"])
                )

                index += 1

                continue

            # ---------------- normal paragraph ----------------

            elements.append(
                self._para(stripped, styles["body"])
            )

            index += 1

        doc.build(elements)