import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle


# ============================================================
# ✅ Enhanced Chart Generator (Bar + Donut + Line + Average)
# ============================================================

def generate_charts(summary, dataset_id):
    chart_dir = "uploads/charts/"
    os.makedirs(chart_dir, exist_ok=True)

    labels = list(summary["type_distribution"].keys())
    values = list(summary["type_distribution"].values())

    palette = ["#2563eb", "#22c55e", "#f97316", "#ef4444", "#a855f7", "#8b5cf6", "#06b6d4"]

    # ✅ Bar Chart - Enhanced
    bar_path = f"{chart_dir}bar_{dataset_id}.png"
    plt.figure(figsize=(8, 4.5))
    bars = plt.bar(labels, values, color=palette[:len(labels)], edgecolor='black', linewidth=0.7, alpha=0.85)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.title("Equipment Distribution", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("Count", fontsize=11, fontweight='bold')
    plt.xlabel("Equipment Type", fontsize=11, fontweight='bold')
    plt.xticks(rotation=25, ha='right')
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(bar_path, dpi=150, bbox_inches='tight')
    plt.close()

    # ✅ Donut Pie Chart - Enhanced
    pie_path = f"{chart_dir}pie_{dataset_id}.png"
    plt.figure(figsize=(7, 5))
    
    # Create donut with better styling
    wedges, texts, autotexts = plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=palette[:len(labels)],
        pctdistance=0.82,
        textprops={'fontsize': 10, 'weight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )

    # Style percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)

    centre_circle = plt.Circle((0, 0), 0.60, fc="white", linewidth=2, edgecolor='#cccccc')
    plt.gca().add_artist(centre_circle)

    plt.title("Equipment Distribution (%)", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(pie_path, dpi=150, bbox_inches='tight')
    plt.close()

    # ✅ NEW: Line Chart - Performance Metrics Trend
    line_path = f"{chart_dir}line_{dataset_id}.png"
    plt.figure(figsize=(8, 4.5))
    
    # Create sample trend data (you can replace with actual data)
    metrics = ['Flowrate', 'Pressure', 'Temperature']
    avg_values = [
        float(str(summary["avg_flowrate"]).split()[0]),
        float(str(summary["avg_pressure"]).split()[0]),
        float(str(summary["avg_temperature"]).split()[0])
    ]
    
    # Normalize values for better visualization
    max_val = max(avg_values)
    normalized = [v/max_val * 100 for v in avg_values]
    
    plt.plot(metrics, normalized, marker='o', linewidth=2.5, markersize=10, 
             color='#2563eb', markerfacecolor='#ef4444', markeredgewidth=2, markeredgecolor='#2563eb')
    
    # Add value labels
    for i, (metric, val, norm) in enumerate(zip(metrics, avg_values, normalized)):
        plt.text(i, norm + 3, f'{val:.2f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')
    
    plt.title("Average Performance Metrics", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("Normalized Value (%)", fontsize=11, fontweight='bold')
    plt.xlabel("Metric Type", fontsize=11, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.ylim(0, 110)
    plt.tight_layout()
    plt.savefig(line_path, dpi=150, bbox_inches='tight')
    plt.close()

    # ✅ NEW: Statistics Summary Chart
    stats_path = f"{chart_dir}stats_{dataset_id}.png"
    plt.figure(figsize=(8, 4.5))
    
    categories = ['Total\nEquipment', 'Avg\nFlowrate', 'Avg\nPressure', 'Avg\nTemperature']
    values_display = [
        summary["total_count"],
        float(str(summary["avg_flowrate"]).split()[0]),
        float(str(summary["avg_pressure"]).split()[0]),
        float(str(summary["avg_temperature"]).split()[0])
    ]
    
    # Create horizontal bar chart
    bars = plt.barh(categories, values_display, color=['#2563eb', '#22c55e', '#f97316', '#ef4444'], 
                    edgecolor='black', linewidth=0.7, alpha=0.85)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values_display)):
        plt.text(val + max(values_display) * 0.02, bar.get_y() + bar.get_height()/2, 
                f'{val:.2f}', va='center', fontsize=10, fontweight='bold')
    
    plt.title("Key Performance Indicators", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Value", fontsize=11, fontweight='bold')
    plt.grid(axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(stats_path, dpi=150, bbox_inches='tight')
    plt.close()

    return bar_path, pie_path, line_path, stats_path


# ============================================================
# ✅ ENHANCED PDF REPORT GENERATOR
# ============================================================

def generate_pdf(dataset, pdf_path):
    summary = dataset.summary
    dataset_id = dataset.id

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    today = datetime.now().strftime("%d %B %Y")

    left_margin = 60
    right_margin = width - 60
    bottom_margin = 70
    top_margin = height - 70
    spacing = 50

    # ✅ Helper: New page if space runs out
    def check_page_space(y, required=120):
        if y < bottom_margin + required:
            c.showPage()
            return top_margin
        return y

    # ✅ Helper: Draw header on each page
    def draw_header():
        c.setStrokeColor(colors.HexColor("#2563eb"))
        c.setLineWidth(2)
        c.line(left_margin, height - 50, right_margin, height - 50)
        
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor("#64748b"))
        c.drawString(left_margin, height - 40, "Chemical Equipment Analysis Report")
        c.drawRightString(right_margin, height - 40, today)

    # ============================================================
    # ✅ PAGE 1 — PROFESSIONAL COVER PAGE
    # ============================================================

    # Background rectangle
    c.setFillColor(colors.HexColor("#2563eb"))
    c.rect(0, height - 250, width, 250, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width / 2, height - 120, "EQUIPMENT ANALYSIS")

    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 160, "REPORT")

    # Divider line
    c.setStrokeColor(colors.white)
    c.setLineWidth(2)
    c.line(width/2 - 150, height - 180, width/2 + 150, height - 180)

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height / 2 + 40, "Comprehensive Analytics & Visualization Summary")

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, height / 2 - 10, f"Dataset: {dataset.filename}")

    # Footer info
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(width / 2, 100, f"Report Generated: {today}")

    c.showPage()

    # ============================================================
    # ✅ PAGE 2 — TABLE OF CONTENTS
    # ============================================================

    draw_header()
    y = top_margin - 30

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.black)
    c.drawString(left_margin, y, "Table of Contents")
    y -= 40

    toc_items = [
        ("1.", "Report Overview", "3"),
        ("2.", "Dataset Preview", "3"),
        ("3.", "Summary Statistics", "4"),
        ("4.", "Equipment Distribution", "4"),
        ("5.", "Performance Metrics Analysis", "5"),
        ("6.", "Visualization Charts", "6"),
    ]

    c.setFont("Helvetica", 12)
    for num, title, page in toc_items:
        c.drawString(left_margin + 20, y, f"{num}  {title}")
        c.drawRightString(right_margin - 20, y, page)
        
        # Dotted line
        c.setDash(2, 2)
        c.line(left_margin + 220, y + 2, right_margin - 50, y + 2)
        c.setDash()
        
        y -= 30

    c.showPage()

    # ============================================================
    # ✅ PAGE 3+ — REPORT CONTENT
    # ============================================================

    draw_header()
    y = top_margin - 30

    # ------------------------------------------------------------
    # 1. Report Overview
    # ------------------------------------------------------------

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#2563eb"))
    c.drawString(left_margin, y, "1. Report Overview")
    
    c.setStrokeColor(colors.HexColor("#2563eb"))
    c.setLineWidth(1)
    c.line(left_margin, y - 5, left_margin + 150, y - 5)
    
    y -= 30

    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawString(left_margin, y, "This comprehensive report provides detailed analytical insights into the uploaded chemical")
    y -= 18
    c.drawString(left_margin, y, "equipment dataset, including statistical summaries, distribution analysis, and performance metrics.")
    y -= 30

    overview_points = [
        "• Complete dataset preview with all recorded parameters",
        "• Statistical analysis of key performance indicators (KPIs)",
        "• Equipment type distribution and composition breakdown",
        "• Performance trends and comparative analysis",
        "• Professional visualization charts and graphs"
    ]

    c.setFont("Helvetica", 10)
    for point in overview_points:
        y = check_page_space(y, 40)
        c.drawString(left_margin + 20, y, point)
        y -= 22

    y -= spacing

    # ------------------------------------------------------------
    # 2. Dataset Preview
    # ------------------------------------------------------------

    y = check_page_space(y, 280)
    
    if y == top_margin:
        draw_header()
        y -= 30

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#2563eb"))
    c.drawString(left_margin, y, "2. Uploaded Dataset Preview")
    
    c.setLineWidth(1)
    c.line(left_margin, y - 5, left_margin + 200, y - 5)
    
    y -= 35

    preview = summary.get("data_preview", [])

    if preview:
        columns = list(preview[0].keys())
        rows = [list(r.values()) for r in preview[:6]]  # Limit to 6 rows for better fit
        table_data = [columns] + rows

        data_table = Table(table_data, repeatRows=1)

        data_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ("LINEBELOW", (0, 0), (-1, 0), 2, colors.HexColor("#1e40af")),
        ]))

        data_table.wrapOn(c, width, height)
        data_table.drawOn(c, left_margin, y - 180)
        y -= 220

    else:
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(left_margin, y, "No preview data available.")
        y -= 40

    y -= spacing

    # ------------------------------------------------------------
    # 3. Summary Statistics
    # ------------------------------------------------------------

    y = check_page_space(y, 230)
    
    if y == top_margin:
        draw_header()
        y -= 30

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#2563eb"))
    c.drawString(left_margin, y, "3. Summary Statistics")
    
    c.setLineWidth(1)
    c.line(left_margin, y - 5, left_margin + 170, y - 5)
    
    y -= 35

    stats_data = [
        ["Performance Metric", "Value", "Unit"],
        ["Total Equipment Count", str(summary["total_count"]), "units"],
        ["Average Flowrate", str(summary["avg_flowrate"]).split()[0], "m³/h"],
        ["Average Pressure", str(summary["avg_pressure"]).split()[0], "bar"],
        ["Average Temperature", str(summary["avg_temperature"]).split()[0], "°C"],
    ]

    stats_table = Table(stats_data, colWidths=[200, 120, 80])

    stats_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("LINEBELOW", (0, 0), (-1, 0), 2, colors.HexColor("#1e40af")),
    ]))

    stats_table.wrapOn(c, width, height)
    stats_table.drawOn(c, left_margin, y - 130)
    y -= 180

    y -= spacing

    # ------------------------------------------------------------
    # 4. Equipment Distribution
    # ------------------------------------------------------------

    y = check_page_space(y, 230)
    
    if y == top_margin:
        draw_header()
        y -= 30

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#2563eb"))
    c.drawString(left_margin, y, "4. Equipment Distribution Analysis")
    
    c.setLineWidth(1)
    c.line(left_margin, y - 5, left_margin + 250, y - 5)
    
    y -= 35

    dist = summary["type_distribution"]

    dist_data = [["Equipment Type", "Count", "Percentage"]]
    total = sum(dist.values())
    
    for eq_type, count in dist.items():
        percentage = f"{(count/total)*100:.1f}%"
        dist_data.append([eq_type, str(count), percentage])

    dist_table = Table(dist_data, colWidths=[200, 100, 100])

    dist_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),

        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("LINEBELOW", (0, 0), (-1, 0), 2, colors.HexColor("#1e40af")),
    ]))

    dist_table.wrapOn(c, width, height)
    dist_table.drawOn(c, left_margin, y - (len(dist_data) * 25))
    
    y -= (len(dist_data) * 25) + 30
    y -= spacing

    # ------------------------------------------------------------
    # 5. Visualization Charts
    # ------------------------------------------------------------

    c.showPage()
    draw_header()
    y = top_margin - 30

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#2563eb"))
    c.drawString(left_margin, y, "5. Visualization & Analysis Charts")
    
    c.setLineWidth(1)
    c.line(left_margin, y - 5, left_margin + 260, y - 5)
    
    y -= 40

    bar_path, pie_path, line_path, stats_path = generate_charts(summary, dataset_id)

    # Chart 1: Bar Chart
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y, "Equipment Distribution - Bar Chart")
    y -= 10
    
    c.drawImage(bar_path, left_margin, y - 240, width=460, height=230)
    y -= 260

    # Chart 2: Donut Chart
    y = check_page_space(y, 270)
    if y == top_margin:
        draw_header()
        y -= 30
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y, "Equipment Distribution - Percentage Breakdown")
    y -= 10
    
    c.drawImage(pie_path, left_margin + 50, y - 240, width=380, height=230)
    y -= 260

    # Chart 3: Line Chart (New Page)
    c.showPage()
    draw_header()
    y = top_margin - 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y, "Performance Metrics - Trend Analysis")
    y -= 10
    
    c.drawImage(line_path, left_margin, y - 240, width=460, height=230)
    y -= 260

    # Chart 4: KPI Stats
    y = check_page_space(y, 270)
    if y == top_margin:
        draw_header()
        y -= 30
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y, "Key Performance Indicators - Summary")
    y -= 10
    
    c.drawImage(stats_path, left_margin, y - 240, width=460, height=230)

    # ✅ Save
    c.save()