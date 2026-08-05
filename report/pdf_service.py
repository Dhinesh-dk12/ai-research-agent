from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from reportlab.lib.enums import (
    TA_CENTER,
)


class PDFService:

    def generate_pdf(
        self,
        markdown_text: str,
        output_path: str,
    ):

        doc = SimpleDocTemplate(
            output_path
        )

        styles = getSampleStyleSheet()

        title_style = styles["Heading1"]
        title_style.alignment = TA_CENTER

        heading_style = styles["Heading2"]

        sub_heading_style = styles["Heading3"]

        body_style = styles["BodyText"]

        bullet_style = styles["Bullet"]

        elements = []

        for line in markdown_text.splitlines():

            line = line.strip()

            if not line:

                elements.append(
                    Spacer(
                        1,
                        12,
                    )
                )

                continue

            # --------------------------
            # H1
            # --------------------------

            if line.startswith("# "):

                elements.append(

                    Paragraph(

                        line[2:],

                        title_style,

                    )

                )

                continue

            # --------------------------
            # H2
            # --------------------------

            if line.startswith("## "):

                elements.append(

                    Paragraph(

                        line[3:],

                        heading_style,

                    )

                )

                continue

            # --------------------------
            # H3
            # --------------------------

            if line.startswith("### "):

                elements.append(

                    Paragraph(

                        line[4:],

                        sub_heading_style,

                    )

                )

                continue

            # --------------------------
            # Bullet
            # --------------------------

            if line.startswith("- "):

                elements.append(

                    Paragraph(

                        f"• {line[2:]}",

                        bullet_style,

                    )

                )

                continue

            # --------------------------
            # Numbered List
            # --------------------------

            if (
                len(line) > 2
                and line[0].isdigit()
                and line[1] == "."
            ):

                elements.append(

                    Paragraph(

                        line,

                        body_style,

                    )

                )

                continue

            # --------------------------
            # Normal Paragraph
            # --------------------------

            elements.append(

                Paragraph(

                    line,

                    body_style,

                )

            )

        doc.build(
            elements
        )