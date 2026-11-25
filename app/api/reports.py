
from io import BytesIO

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from app.services.repository_student_service import get_students
from app.services.repository_faculty_service import get_faculty
from app.services.repository_course_service import get_courses
from app.services.repository_enrollment_service import get_enrollments


router = APIRouter(prefix="/reports", tags=["Reports"])


REPORTS = {
    "students": {
        "title": "Students Report",
        "columns": ["Student ID", "Name", "Age", "Email", "Department"],
        "fields": ["student_id", "name", "age", "email", "department"],
        "function": get_students,
    },
    "faculty": {
        "title": "Faculty Report",
        "columns": ["Faculty ID", "Name", "Age", "Email", "Department"],
        "fields": ["faculty_id", "name", "age", "email", "department"],
        "function": get_faculty,
    },
    "courses": {
        "title": "Courses Report",
        "columns": ["Course Code", "Course Name", "Credits"],
        "fields": ["course_code", "course_name", "credits"],
        "function": get_courses,
    },
    "enrollments": {
        "title": "Enrollments Report",
        "columns": ["Enrollment ID", "Student ID", "Course Code"],
        "fields": ["enrollment_id", "student_id", "course_code"],
        "function": get_enrollments,
    },
}


def get_report_data(report_type):
    if report_type not in REPORTS:
        raise HTTPException(
            status_code=404,
            detail="Report type not found."
        )

    config = REPORTS[report_type]
    records = config["function"]()

    rows = []

    for record in records:
        row = []

        for field in config["fields"]:
            value = getattr(record, field, "")
            row.append("" if value is None else str(value))

        rows.append(row)

    return config, rows


@router.get("/{report_type}/pdf")
def download_pdf(report_type: str):
    config, rows = get_report_data(report_type)

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    content = [
        Paragraph(config["title"], styles["Title"]),
        Spacer(1, 20)
    ]

    table_data = [config["columns"]]

    if rows:
        table_data.extend(rows)
    else:
        table_data.append(["No records found"] + [""] * (len(config["columns"]) - 1))

    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243b64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#edf2f7")
        ]),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    content.append(table)

    content.append(Spacer(1, 15))
    content.append(
        Paragraph(f"Total Records: {len(rows)}", styles["Normal"])
    )

    document.build(content)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{report_type}_report.pdf"'
        }
    )


@router.get("/{report_type}/excel")
def download_excel(report_type: str):
    config, rows = get_report_data(report_type)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = config["title"][:31]

    sheet.append(config["columns"])

    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="243B64"
        )
        cell.alignment = Alignment(horizontal="center")

    for row in rows:
        sheet.append(row)

    for column in sheet.columns:
        max_length = max(
            len(str(cell.value or ""))
            for cell in column
        )
        sheet.column_dimensions[column[0].column_letter].width = min(
            max_length + 4,
            40
        )

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{report_type}_report.xlsx"'
        }
    )
