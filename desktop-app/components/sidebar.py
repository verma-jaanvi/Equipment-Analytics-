"""
Sidebar component - orchestration & history
"""

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QWidget
from PyQt5.QtCore import Qt, pyqtSignal


class Sidebar(QFrame):
    """
    Sidebar component with actions and history
    """
    
    # Signals
    upload_clicked = pyqtSignal()
    download_clicked = pyqtSignal()
    logout_clicked = pyqtSignal()
    history_item_double_clicked = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar UI"""
        self.setFixedWidth(380)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-right: 1px solid #e5e7eb;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Blue header with icon
        header = self.create_header()
        main_layout.addWidget(header)

        # Actions section
        actions_section = self.create_actions_section()
        main_layout.addWidget(actions_section)

        # Recent uploads section
        history_section = self.create_history_section()
        main_layout.addWidget(history_section)

        # Spacer
        main_layout.addStretch()

        # Logout button
        logout_section = self.create_logout_section()
        main_layout.addWidget(logout_section)

        self.setLayout(main_layout)
    
    def create_header(self):
        """Create blue header with icon"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:1 #3b82f6);
                border-radius: 0;
                padding: 30px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        logo = QLabel("📊")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            font-size: 48px;
            background: rgba(255,255,255,0.2);
            border-radius: 16px;
            padding: 20px;
        """)
        
        layout.addWidget(logo)
        header.setLayout(layout)
        
        return header
    
    def create_actions_section(self):
        """Create actions section"""
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 30, 24, 20)
        layout.setSpacing(16)

        actions_label = QLabel("ACTIONS")
        actions_label.setStyleSheet("""
            font-size: 12px;
            font-weight: 700;
            color: #6b7280;
            letter-spacing: 1px;
        """)

        self.upload_btn = QPushButton("📂  Upload Dataset")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background: #2563eb;
                color: white;
                text-align: left;
                padding: 14px 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background: #1d4ed8;
            }
        """)
        self.upload_btn.clicked.connect(self.upload_clicked.emit)

        self.download_btn = QPushButton("⬇  Download Report")
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background: #f59e0b;
                color: white;
                text-align: left;
                padding: 14px 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background: #d97706;
            }
            QPushButton:disabled {
                background: #d1d5db;
                color: #9ca3af;
            }
        """)
        self.download_btn.clicked.connect(self.download_clicked.emit)

        layout.addWidget(actions_label)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.download_btn)

        container.setLayout(layout)
        return container
    
    def create_history_section(self):
        """Create recent uploads history section"""
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(12)

        header = QHBoxLayout()
        
        icon = QLabel("🕒")
        icon.setStyleSheet("font-size: 18px;")
        
        title = QLabel("Recent Uploads")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1f2937;
        """)
        
        header.addWidget(icon)
        header.addWidget(title)
        header.addStretch()

        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.history_item_double_clicked.emit)

        layout.addLayout(header)
        layout.addWidget(self.history_list)

        container.setLayout(layout)
        return container
    
    def create_logout_section(self):
        """Create logout button section"""
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 0, 24, 24)

        logout_btn = QPushButton("🚪  Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: #ef4444;
                color: white;
                font-size: 15px;
                font-weight: 700;
                padding: 14px 20px;
                text-align: left;
            }
            QPushButton:hover {
                background: #dc2626;
            }
        """)
        logout_btn.clicked.connect(self.logout_clicked.emit)

        layout.addWidget(logout_btn)
        container.setLayout(layout)
        
        return container
    
    def enable_download(self, enabled=True):
        """Enable or disable download button"""
        self.download_btn.setEnabled(enabled)
    
    def load_history(self, history_data):
        """Load history items"""
        self.history_list.clear()
        for item in history_data:
            self.history_list.addItem(f"Dataset-report {item['id']}")
    
    def clear_history(self):
        """Clear all history items"""
        self.history_list.clear()