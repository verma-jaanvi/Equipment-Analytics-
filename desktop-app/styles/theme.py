"""
Global theme configuration and stylesheet definitions
"""

# Color Palette
COLORS = {
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',
    'primary_light': '#3b82f6',
    'secondary': '#f59e0b',
    'secondary_hover': '#d97706',
    'danger': '#ef4444',
    'danger_hover': '#dc2626',
    'success': '#10b981',
    'background': '#f2f6fb',
    'card_background': 'white',
    'text_primary': '#0f172a',
    'text_secondary': '#6b7280',
    'text_tertiary': '#475569',
    'border': '#d0d7e2',
    'border_light': '#e5e7eb',
    'stat_bg': '#f8fafc',
    'disabled': '#d1d5db',
    'disabled_text': '#9ca3af',
}

# Global Application Stylesheet
GLOBAL_STYLESHEET = f"""
    QWidget {{
        background: {COLORS['background']};
        font-family: "Segoe UI";
        color: {COLORS['text_primary']};
    }}

    QLineEdit {{
        padding: 16px;
        border-radius: 14px;
        border: 1px solid {COLORS['border']};
        font-size: 16px;
        background: white;
    }}

    QPushButton {{
        border: none;
        border-radius: 14px;
        padding: 16px;
        font-size: 16px;
        font-weight: 800;
        background: {COLORS['primary']};
        color: white;
    }}

    QPushButton:hover {{
        background: {COLORS['primary_hover']};
    }}

    QListWidget {{
        border-radius: 16px;
        border: 1px solid {COLORS['border']};
        background: white;
        font-size: 15px;
        padding: 12px;
    }}

    QListWidget::item {{
        padding: 10px;
        border-radius: 6px;
        margin: 2px 0;
    }}

    QListWidget::item:hover {{
        background: #f3f4f6;
    }}

    QListWidget::item:selected {{
        background: #dbeafe;
        color: #1e40af;
    }}
"""

# Table Stylesheet
# ✅ Dataset Preview Table UI (Exactly Like Screenshot)

TABLE_STYLESHEET = f"""
QTableWidget {{
    background: white;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    font-size: 15px;
    gridline-color: #e2e8f0;
}}

QHeaderView::section {{
    background: {COLORS['primary']};
    color: white;
    font-weight: 900;
    font-size: 14px;
    padding: 16px;
    border: none;
}}

QTableWidget::item {{
    background: white;
    padding: 14px;
    border-bottom: 1px solid #e2e8f0;
}}

QTableWidget::item:selected {{
    background: #dbeafe;
    color: black;
}}
"""

# Scroll Area Stylesheet
SCROLL_AREA_STYLESHEET = f"""
    QScrollArea {{
        border: none;
        background: {COLORS['background']};
    }}
"""