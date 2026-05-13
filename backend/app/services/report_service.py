import os
import pandas as pd

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from reportlab.lib.styles import getSampleStyleSheet


REPORT_FOLDER = "reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)


def generate_excel_report(df, filename):

    report_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    df.to_excel(
        report_path,
        index=False
    )

    return report_path


def generate_pdf_report(df, filename):

    report_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    doc = SimpleDocTemplate(report_path)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Sales Forecast Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    summary = Paragraph(
        f"Total Rows: {len(df)}",
        styles["BodyText"]
    )

    elements.append(summary)

    elements.append(Spacer(1, 20))

    for index, row in df.head(10).iterrows():

        row_text = Paragraph(
            str(row.to_dict()),
            styles["BodyText"]
        )

        elements.append(row_text)

        elements.append(Spacer(1, 10))

    doc.build(elements)

    return report_path