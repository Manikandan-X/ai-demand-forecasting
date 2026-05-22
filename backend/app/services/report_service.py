import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from openpyxl import Workbook
from openpyxl.styles import Font


REPORT_FOLDER = "reports"

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ANALYTICS SUMMARY
def generate_analytics_summary(df):

    summary = {

        "total_sales":
            float(
                df["Total_Amount"].sum()
            ),

        "total_orders":
            int(len(df)),

        "top_product":
            df["Product"]
            .value_counts()
            .idxmax(),

        "average_order_value":
            float(
                df["Total_Amount"]
                .mean()
            )
    }

    return summary


# EXCEL REPORT
def generate_excel_report(
    df,
    filename
):

    report_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Forecast Report"

    # TITLE
    sheet["A1"] = (
        "AI Forecast Analytics Report"
    )

    sheet["A1"].font = Font(
        bold=True,
        size=16
    )

    summary = generate_analytics_summary(df)

    # SUMMARY SECTION
    sheet["A3"] = "Total Sales"
    sheet["B3"] = summary[
        "total_sales"
    ]

    sheet["A4"] = "Total Orders"
    sheet["B4"] = summary[
        "total_orders"
    ]

    sheet["A5"] = "Top Product"
    sheet["B5"] = summary[
        "top_product"
    ]

    sheet["A6"] = (
        "Average Order Value"
    )

    sheet["B6"] = summary[
        "average_order_value"
    ]

    # DATA HEADER
    start_row = 9

    for col_num, column_name in enumerate(
        df.columns,
        1
    ):

        cell = sheet.cell(
            row=start_row,
            column=col_num
        )

        cell.value = column_name

        cell.font = Font(
            bold=True
        )

    # DATA ROWS
    for row_index, row in enumerate(
        df.values,
        start_row + 1
    ):

        for col_index, value in enumerate(
            row,
            1
        ):

            sheet.cell(
                row=row_index,
                column=col_index,
                value=str(value)
            )

    workbook.save(report_path)

    return report_path


# PDF REPORT
def generate_pdf_report(
    df,
    filename
):

    report_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    document = SimpleDocTemplate(
        report_path
    )

    styles = getSampleStyleSheet()

    elements = []

    # TITLE
    title = Paragraph(
        "AI Forecast Analytics Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    summary = generate_analytics_summary(df)

    # SUMMARY SECTION
    elements.append(

        Paragraph(
            f"Total Sales: "
            f"{summary['total_sales']}",

            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(

        Paragraph(
            f"Total Orders: "
            f"{summary['total_orders']}",

            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(

        Paragraph(
            f"Top Product: "
            f"{summary['top_product']}",

            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(

        Paragraph(
            f"Average Order Value: "
            f"{summary['average_order_value']}",

            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # SAMPLE DATA
    sample_title = Paragraph(
        "Sample Dataset Records",
        styles["Heading2"]
    )

    elements.append(sample_title)

    elements.append(
        Spacer(1, 10)
    )

    for _, row in df.head(10).iterrows():

        row_text = Paragraph(
            str(row.to_dict()),
            styles["BodyText"]
        )

        elements.append(row_text)

        elements.append(
            Spacer(1, 8)
        )

    document.build(elements)

    return report_path