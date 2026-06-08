from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from logger_config import logger
import os
from datetime import datetime
import kaleido

def generate_pdf_report(user_question,sql_query,insights,data,fig):
    try:
        logger.info("Initiating pdf report generation.")
        # ============================================
        # FILE PATHS
        # ============================================
        BASE_DIR = os.path.dirname(__file__)
        logger.info(f"BASE_DIR : {BASE_DIR}")
        reports_file = f"businessintel_report_{datetime.now().strftime('%Y%m%d_%H_%M')}.pdf"
        pdf_file_path = os.path.join(BASE_DIR, 'reports', reports_file)
        chart_image_path = f"chart_image_{datetime.now().strftime('%Y%m%d_%H_%M')}.png"
        logger.info(f"pdf_file_path : {pdf_file_path}")
        # ============================================
        # SAVE CHART AS IMAGE
        # ============================================
        fig.write_image(chart_image_path)

        # ============================================
        # CREATE PDF DOCUMENT
        # ============================================
        document = SimpleDocTemplate(
            pdf_file_path,
            pagesize=letter,
            title="BusinessIntel AI Report",
            author="BusinessIntel AI",
            subject="AI Generated Business Analytics Report"
        )
        styles = getSampleStyleSheet()
        elements = []

        # ============================================
        # TITLE
        # ============================================
        title = Paragraph(
            "<b>BusinessIntel AI Report</b>",
            styles['Title']
        )
        elements.append(title)
        elements.append(Spacer(1, 20))

        # ============================================
        # BUSINESS QUESTION
        # ============================================
        question_heading = Paragraph(
            "<b>Business Question:</b>",
            styles['Heading2']
        )
        question_text = Paragraph(
            user_question,
            styles['BodyText']
        )
        elements.append(question_heading)
        elements.append(question_text)
        elements.append(Spacer(1, 12))

        # ============================================
        # SQL QUERY
        # ============================================
        sql_heading = Paragraph(
            "<b>Generated SQL Query:</b>",
            styles['Heading2']
        )
        sql_text = Paragraph(
            sql_query.replace("\n", "<br/>"),
            styles['BodyText']
        )
        elements.append(sql_heading)
        elements.append(sql_text)
        elements.append(Spacer(1, 12))

        # ============================================
        # AI INSIGHTS
        # ============================================
        insight_heading = Paragraph(
            "<b>AI Business Insights:</b>",
            styles['Heading2']
        )
        insight_text = Paragraph(
            insights.replace("\n", "<br/>"),
            styles['BodyText']
        )
        elements.append(insight_heading)
        elements.append(insight_text)
        elements.append(Spacer(1, 20))

        # ============================================
        # CHART IMAGE
        # ============================================
        chart_heading = Paragraph(
            "<b>Generated Chart:</b>",
            styles['Heading2']
        )
        elements.append(chart_heading)
        elements.append(Spacer(1, 12))

        chart_image = Image(
            chart_image_path,
            width=6*inch,
            height=4*inch
        )
        elements.append(chart_image)
        elements.append(Spacer(1, 20))

        # ============================================
        # DATA TABLE
        # ============================================
        data_heading = Paragraph(
            "<b>Query Result Data:</b>",
            styles['Heading2']
        )
        elements.append(data_heading)
        elements.append(Spacer(1, 12))
        formatted_data = data.copy()
        for column in formatted_data.columns:
            formatted_data[column] = formatted_data[column].apply(
                lambda x: str(int(x)) if isinstance(x, float) and x.is_integer() else str(x))
        table_data = [formatted_data.columns.tolist()] + formatted_data.head(20).values.tolist()
        #table_data = ([data.columns.tolist()] + data.head(20).values.tolist())
        table = Table(table_data)
        table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
        )
        elements.append(table)

        # ============================================
        # BUILD PDF
        # ============================================
        document.build(elements)
        # ============================================
        # CLEANUP IMAGE FILE
        # ============================================
        if os.path.exists(chart_image_path):
            logger.info(f"chart_image_path exists : {chart_image_path}")
            os.remove(chart_image_path)
            logger.info("chart image path removed.")
        logger.info(f"pdf_file_path created : {pdf_file_path}")
        return pdf_file_path
    except Exception as e:
        logger.exception(f"PDF Report Generation Error : {e}")
        return None


def generate_csv_file(csv_data):
    try:
        logger.info("Initiating csv file generation")
        BASE_DIR = os.path.dirname(__file__)
        logger.info(f"BASE_DIR : {BASE_DIR}")
        reports_path = os.path.join(BASE_DIR, 'reports')
        csv_file_name = f"businessintel_data_{datetime.now().strftime('%Y%m%d_%H_%M')}.csv"
        csv_file_path = os.path.join(reports_path, csv_file_name)
        csv_data.to_csv(csv_file_path, index=False)
        logger.info("csv file saved successfully.")
        return csv_file_path
    except Exception as e:
        logger.exception(f"generate_csv_file : {e}")
        return None
