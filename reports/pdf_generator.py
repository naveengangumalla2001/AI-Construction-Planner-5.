from io import BytesIO
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# -----------------------------------------------------
# Font setup: built-in Helvetica has no rupee (₹) glyph,
# so try a Unicode TTF font and fall back to "Rs." if none found.
# -----------------------------------------------------

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
RUPEE = "Rs. "

_FONT_CANDIDATES = [
    (
        "DejaVuSans",
        "DejaVuSans-Bold",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
    (
        "DejaVuSans",
        "DejaVuSans-Bold",
        "DejaVuSans.ttf",  # place font files next to this script
        "DejaVuSans-Bold.ttf",
    ),
    (
        "ArialUnicode",
        "ArialUnicode-Bold",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ),
]

for _reg, _bold, _reg_path, _bold_path in _FONT_CANDIDATES:
    if os.path.exists(_reg_path) and os.path.exists(_bold_path):
        try:
            pdfmetrics.registerFont(TTFont(_reg, _reg_path))
            pdfmetrics.registerFont(TTFont(_bold, _bold_path))
            FONT_REGULAR, FONT_BOLD, RUPEE = _reg, _bold, "₹"
            break
        except Exception:
            continue


def money(value, decimals=2):
    """Format a number as currency."""
    try:
        return f"{RUPEE}{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return f"{RUPEE}0"


def generate_project_report(
    project_name,
    location,
    plot_area,
    builtup_area,
    floors,
    bedrooms,
    bathrooms,
    construction_quality,
    material_quality,
    parking,
    predicted_cost,
    material_cost,
    labour_cost,
    other_cost,
    materials,
    timeline,
    start_date,
    completion_date,
    budget_optimization=None,
):
    """
    Generate a PDF construction planning report.
    """

    # -----------------------------------------------------
    # Create PDF in memory
    # -----------------------------------------------------

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName=FONT_BOLD,
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=15,
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName=FONT_BOLD,
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=14,
    )

    story = []

    # =====================================================
    # TITLE
    # =====================================================

    story.append(Paragraph("AI-Powered Smart Construction Planner", title_style))

    story.append(
        Paragraph(
            "Construction Planning & Cost Estimation Report",
            ParagraphStyle(
                "Subtitle",
                parent=normal_style,
                alignment=TA_CENTER,
                fontSize=11,
            ),
        )
    )

    story.append(Spacer(1, 20))

    # =====================================================
    # 1. PROJECT DETAILS
    # =====================================================

    story.append(Paragraph("1. Project Details", heading_style))

    project_data = [
        ["Project Name", project_name],
        ["Location", location],
        ["Plot Area", f"{plot_area:,.0f} sqft"],
        ["Built-up Area", f"{builtup_area:,.0f} sqft"],
        ["Number of Floors", str(floors)],
        ["Bedrooms", str(bedrooms)],
        ["Bathrooms", str(bathrooms)],
        ["Construction Quality", construction_quality],
        ["Material Quality", material_quality],
        ["Parking", parking],
        ["Project Start Date", start_date.strftime("%d-%m-%Y")],
        ["Estimated Completion Date", completion_date.strftime("%d-%m-%Y")],
    ]

    project_table = Table(project_data, colWidths=[2.4 * inch, 3.5 * inch])

    project_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
            ("FONTNAME", (1, 0), (1, -1), FONT_REGULAR),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(project_table)

    # =====================================================
    # 2. COST ESTIMATION
    # =====================================================

    story.append(Paragraph("2. Construction Cost Estimation", heading_style))

    cost_data = [
        ["Cost Category", "Estimated Cost"],
        ["Material Cost", money(material_cost)],
        ["Labour Cost", money(labour_cost)],
        ["Other Costs", money(other_cost)],
        ["Total Construction Cost", money(predicted_cost)],
    ]

    cost_table = Table(cost_data, colWidths=[3.5 * inch, 2.4 * inch])

    cost_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BACKGROUND", (0, 4), (-1, 4), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), FONT_REGULAR),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("FONTNAME", (0, 4), (-1, 4), FONT_BOLD),
            ("ALIGN", (1, 1), (1, -1), "RIGHT"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(cost_table)
    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Estimated Total Cost: {money(predicted_cost)}",
            ParagraphStyle(
                "CostHighlight",
                parent=normal_style,
                fontSize=12,
                leading=16,
            ),
        )
    )

    # =====================================================
    # 3. MATERIAL ESTIMATION
    # =====================================================

    story.append(Paragraph("3. Estimated Construction Materials", heading_style))

    material_data = [["Material", "Estimated Quantity"]]

    for material, quantity in materials.items():
        material_data.append([str(material), str(quantity)])

    material_table = Table(material_data, colWidths=[3.5 * inch, 2.4 * inch])

    material_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), FONT_REGULAR),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(material_table)

    # =====================================================
    # 4. TIMELINE
    # =====================================================

    story.append(Paragraph("4. Estimated Construction Timeline", heading_style))

    timeline_data = [["Construction Phase", "Duration"]]

    for phase, days in timeline.items():
        if phase != "Total":
            timeline_data.append([str(phase), f"{days} days"])

    timeline_data.append([
        "Total Construction Duration",
        f"{timeline.get('Total', 0)} days",
    ])

    timeline_table = Table(timeline_data, colWidths=[3.5 * inch, 2.4 * inch])

    timeline_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), FONT_REGULAR),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("FONTNAME", (0, -1), (-1, -1), FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(timeline_table)

    # =====================================================
    # 5. BUDGET OPTIMIZATION (optional)
    # =====================================================

    section_no = 5

    if budget_optimization:
        scenarios = budget_optimization.get("scenarios", [])
        recommended = budget_optimization.get("recommended")

        if scenarios:
            story.append(
                Paragraph(f"{section_no}. Budget Optimization", heading_style)
            )
            section_no += 1

            table_data = [
                [
                    "Scenario",
                    "Built-up Area",
                    "Floors",
                    "Estimated Cost",
                    "Budget Status",
                ]
            ]

            for scenario in scenarios:
                table_data.append([
                    str(scenario.get("Scenario", "")),
                    str(scenario.get("Built-up Area", "")),
                    str(scenario.get("Floors", "")),
                    money(scenario.get("Estimated Cost", 0), 0),
                    str(scenario.get("Budget Status", "")),
                ])

            budget_table = Table(
                table_data,
                repeatRows=1,
                colWidths=[
                    1.7 * inch,
                    1.0 * inch,
                    0.7 * inch,
                    1.2 * inch,
                    1.3 * inch,
                ],
            )

            budget_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, -1), FONT_REGULAR),
                    ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (3, 1), (3, -1), "RIGHT"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ])
            )

            story.append(budget_table)

            if recommended:
                story.append(Spacer(1, 8))
                story.append(
                    Paragraph(f"<b>Recommended:</b> {recommended}", normal_style)
                )

    # =====================================================
    # PLANNING SUMMARY
    # =====================================================

    story.append(Paragraph(f"{section_no}. Planning Summary", heading_style))

    summary_text = (
        f"The AI Construction Planner estimated the construction "
        f"cost based on the provided project requirements. "
        f"The project has a plot area of {plot_area:,.0f} sqft "
        f"and a built-up area of {builtup_area:,.0f} sqft "
        f"with {floors} floor(s). "
        f"The estimated construction duration is "
        f"{timeline.get('Total', 0)} days."
    )

    story.append(Paragraph(summary_text, normal_style))

    # =====================================================
    # DISCLAIMER
    # =====================================================

    story.append(Spacer(1, 20))
    story.append(Paragraph("Disclaimer", heading_style))

    disclaimer = (
        "Cost, material quantities, floor planning and timeline "
        "outputs are preliminary estimates intended for planning "
        "and demonstration purposes only. The 2D and 3D outputs "
        "are conceptual representations and are not architectural "
        "or structural drawings. Final construction decisions "
        "must be validated by qualified architects, structural "
        "engineers and construction professionals."
    )

    story.append(Paragraph(disclaimer, normal_style))

    # =====================================================
    # BUILD PDF
    # =====================================================

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()