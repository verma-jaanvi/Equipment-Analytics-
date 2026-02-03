"""
Main content area component - statistics, dataset preview table, charts
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont


class ContentArea(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    # ============================================================
    # ✅ UI SETUP
    # ============================================================

    def setup_ui(self):
        from styles import modern_card, TABLE_STYLESHEET
        from components.stat_box import StatBox
        from charts import ChartCanvas

        layout = QVBoxLayout()
        layout.setSpacing(35)
        layout.setContentsMargins(35, 35, 35, 35)

        layout.addLayout(self.create_page_header())
        layout.addWidget(self.create_statistics_card(modern_card, StatBox))
        layout.addWidget(self.create_table_card(modern_card, TABLE_STYLESHEET))
        layout.addWidget(self.create_charts_card(modern_card, ChartCanvas))

        self.setLayout(layout)

    # ============================================================
    # ✅ HEADER
    # ============================================================

    def create_page_header(self):
        header_layout = QVBoxLayout()

        title = QLabel("Equipment Analytics Overview")
        title.setStyleSheet("font-size:40px; font-weight:900;")

        subtitle = QLabel("Comprehensive data analysis and visualization")
        subtitle.setStyleSheet("font-size:16px; color:#6b7280;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        return header_layout

    # ============================================================
    # ✅ STATISTICS CARD
    # ============================================================

    def create_statistics_card(self, modern_card, StatBox):
        card = modern_card()
        layout = QVBoxLayout()

        heading = QLabel("Summary Statistics")
        heading.setStyleSheet("""
            font-size:28px;
            font-weight:900;
            color:#2563eb;
        """)

        grid = QGridLayout()
        grid.setSpacing(25)

        self.total_box = StatBox("Total Equipment")
        self.flow_box = StatBox("Average Flowrate")
        self.pressure_box = StatBox("Average Pressure")
        self.temp_box = StatBox("Average Temperature")

        grid.addWidget(self.total_box, 0, 0)
        grid.addWidget(self.flow_box, 0, 1)
        grid.addWidget(self.pressure_box, 1, 0)
        grid.addWidget(self.temp_box, 1, 1)

        layout.addWidget(heading)
        layout.addLayout(grid)

        self.type_dist_label = QLabel("Upload dataset to view distribution.")
        self.type_dist_label.setStyleSheet("font-size:17px; color:#475569;")
        layout.addWidget(self.type_dist_label)

        card.setLayout(layout)
        return card

    # ============================================================
    # ✅ TABLE CARD - FIXED: NO SCROLL + VISIBLE HEADERS
    # ============================================================

    def create_table_card(self, modern_card, TABLE_STYLESHEET):
        card = modern_card()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        heading = QLabel("Dataset Table Preview (First 10 Rows)")
        heading.setStyleSheet("""
            font-size:28px;
            font-weight:900;
            color:#2563eb;
        """)

        self.data_table = QTableWidget()
        
        # ✅ CRITICAL FIX: Apply stylesheet AFTER creating table
        self.data_table.setStyleSheet(TABLE_STYLESHEET)

        # ✅ Hide row numbers
        self.data_table.verticalHeader().setVisible(False)
        
        # ✅ CRITICAL: Completely disable scrollbars
        self.data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # ✅ CRITICAL: Force horizontal header to be visible
        self.data_table.horizontalHeader().setVisible(True)
        self.data_table.horizontalHeader().setStretchLastSection(True)
        
        # ✅ Stretch all columns evenly
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # ✅ CRITICAL: Set minimum and maximum heights for header
        self.data_table.horizontalHeader().setMinimumHeight(60)
        self.data_table.horizontalHeader().setMaximumHeight(60)
        
        # ✅ Disable editing
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # ✅ Selection
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.setSelectionMode(QTableWidget.SingleSelection)

        # ✅ Visual styling
        self.data_table.setShowGrid(True)
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setFrameShape(QTableWidget.NoFrame)
        
        # ✅ CRITICAL: Set size constraints
        self.data_table.setMinimumHeight(200)
        self.data_table.setMaximumHeight(16777215)  # Allow expansion

        layout.addWidget(heading)
        layout.addWidget(self.data_table)

        card.setLayout(layout)
        return card

    # ============================================================
    # ✅ CHARTS CARD
    # ============================================================

    def create_charts_card(self, modern_card, ChartCanvas):
        card = modern_card()
        layout = QVBoxLayout()

        heading = QLabel("Charts & Visualizations")
        heading.setStyleSheet("""
            font-size:28px;
            font-weight:900;
            color:#2563eb;
        """)

        self.chart_canvas = ChartCanvas()
        self.chart_canvas.setMinimumHeight(650)
        self.chart_canvas.hide()

        layout.addWidget(heading)
        layout.addWidget(self.chart_canvas)

        card.setLayout(layout)
        return card

    # ============================================================
    # ✅ UPDATE STATISTICS
    # ============================================================

    def update_statistics(self, summary):
        self.total_box.update_value(summary["total_count"])
        self.flow_box.update_value(summary["avg_flowrate"])
        self.pressure_box.update_value(summary["avg_pressure"])
        self.temp_box.update_value(summary["avg_temperature"])

        dist_text = "\n".join(
            [f"• {k}: {v}" for k, v in summary["type_distribution"].items()]
        )
        self.type_dist_label.setText("Equipment Distribution:\n\n" + dist_text)

    # ✅ Alias Fix for Dashboard Compatibility
    def update_stats(self, summary):
        """Dashboard calls update_stats → redirect safely"""
        self.update_statistics(summary)

    # ============================================================
    # ✅ UPDATE TABLE - COMPLETELY FIXED
    # ============================================================

    def update_table(self, data_preview):
        if not data_preview:
            return

        # ✅ Limit to 10 rows
        data_preview = data_preview[:10]

        columns = list(data_preview[0].keys())
        
        # ✅ Set columns FIRST
        self.data_table.setColumnCount(len(columns))

        # ✅ CRITICAL: Set header labels with proper formatting
        header_labels = []
        for col in columns:
            # Map to professional names
            col_lower = col.lower()
            if 'equipment' in col_lower and 'name' in col_lower:
                header_labels.append('EQUIPMENT NAME')
            elif col_lower == 'type':
                header_labels.append('TYPE')
            elif 'flow' in col_lower:
                header_labels.append('FLOWRATE')
            elif 'pressure' in col_lower:
                header_labels.append('PRESSURE')
            elif 'temp' in col_lower:
                header_labels.append('TEMPERATURE')
            else:
                # Generic formatting
                header_labels.append(col.replace("_", " ").upper())
        
        self.data_table.setHorizontalHeaderLabels(header_labels)
        
        # ✅ CRITICAL: Force header visibility
        self.data_table.horizontalHeader().setVisible(True)
        self.data_table.horizontalHeader().show()

        # ✅ Set row count
        self.data_table.setRowCount(len(data_preview))

        # ✅ Populate cells
        for row_idx, row_data in enumerate(data_preview):
            for col_idx, col_name in enumerate(columns):
                item = QTableWidgetItem(str(row_data[col_name]))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Set font
                font = QFont("Segoe UI", 14)
                item.setFont(font)
                
                self.data_table.setItem(row_idx, col_idx, item)

        # ✅ CRITICAL FIX: Set row heights BEFORE calculating total
        row_height = 55
        for row in range(self.data_table.rowCount()):
            self.data_table.setRowHeight(row, row_height)

        # ✅ CRITICAL FIX: Calculate exact height needed
        header_height = 60  # We set this explicitly
        total_rows_height = self.data_table.rowCount() * row_height
        border_padding = 10  # Small padding for borders
        
        # ✅ Set BOTH minimum and fixed height
        final_height = header_height + total_rows_height + border_padding
        
        self.data_table.setMinimumHeight(final_height)
        self.data_table.setMaximumHeight(final_height)
        
        # ✅ CRITICAL: Update size hint
        self.data_table.updateGeometry()
        
        # ✅ Force layout update
        self.data_table.verticalScrollBar().hide()

    # ============================================================
    # ✅ UPDATE CHARTS
    # ============================================================

    def update_charts(self, summary):
        self.chart_canvas.show()
        self.chart_canvas.plot_type_distribution(summary)

    # ============================================================
    # ✅ RESET
    # ============================================================

    def reset_all(self):
        self.total_box.reset()
        self.flow_box.reset()
        self.pressure_box.reset()
        self.temp_box.reset()
        self.type_dist_label.setText("Upload dataset to view distribution.")
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        self.data_table.clearContents()
        self.chart_canvas.hide()