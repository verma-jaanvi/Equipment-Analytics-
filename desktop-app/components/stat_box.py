"""
Statistics box widget component
"""

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatBox(QFrame):
    """
    A reusable statistics display box
    """
    
    def __init__(self, title, value="-"):
        """
        Initialize stat box
        
        Args:
            title (str): Stat title/label
            value (str): Stat value (default: "-")
        """
        super().__init__()
        
        self.setStyleSheet("""
            QFrame {
                background: #f8fafc;
                border-radius: 18px;
                padding: 25px;
                border: 1px solid rgba(0,0,0,0.08);
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            font-size: 17px;
            font-weight: 700;
            color: #475569;
        """)

        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("""
            font-size: 36px;
            font-weight: 900;
            color: #0f172a;
        """)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

        self.setLayout(layout)
    
    def update_value(self, value):
        """Update the displayed value"""
        self.value_label.setText(str(value))
    
    def reset(self):
        """Reset value to default"""
        self.value_label.setText("-")