"""
Dashboard component - orchestration & history
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QScrollArea,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt


class Dashboard(QWidget):
    """
    Main dashboard component - orchestration
    """
    
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_dataset_id = None
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Setup dashboard UI"""
        from components.sidebar import Sidebar
        from components.content_area import ContentArea
        from styles import SCROLL_AREA_STYLESHEET
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================================
        # Sidebar
        # ================================
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # ================================
        # Content Area (FIXED SCROLL)
        # ================================
        self.content_area = ContentArea()

        # Wrapper widget INSIDE scroll area
        scroll_container = QWidget()
        scroll_layout = QHBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        scroll_layout.addWidget(self.content_area)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_container)
        scroll.setStyleSheet(SCROLL_AREA_STYLESHEET)

        # ✅ CRITICAL FIX: single scroll only
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
    
    # ============================================================
    # SIGNAL CONNECTIONS
    # ============================================================

    def connect_signals(self):
        """Connect signals"""
        self.sidebar.upload_clicked.connect(self.handle_upload)
        self.sidebar.download_clicked.connect(self.handle_download_current)
        self.sidebar.logout_clicked.connect(self.handle_logout)
        self.sidebar.history_item_double_clicked.connect(self.handle_history_download)
    
    # ============================================================
    # UPLOAD HANDLING
    # ============================================================

    def handle_upload(self):
        """Handle file upload"""
        from api import upload_csv
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select CSV File", 
            "", 
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            response = upload_csv(file_path)
            summary = response["summary"]
            
            self.current_dataset_id = response["dataset_id"]
            
            self.content_area.update_statistics(summary)
            
            preview = summary.get("data_preview", [])
            if preview:
                self.content_area.update_table(preview)
            
            self.content_area.update_charts(summary)
            self.sidebar.enable_download(True)
            self.load_history()
            
        except Exception as e:
            QMessageBox.critical(self, "Upload Failed", str(e))
    
    # ============================================================
    # DOWNLOAD CURRENT REPORT
    # ============================================================

    def handle_download_current(self):
        """Handle download current report"""
        from api import download_report
        
        if not self.current_dataset_id:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report PDF",
            f"report_{self.current_dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if save_path:
            try:
                download_report(self.current_dataset_id, save_path)
            except Exception as e:
                QMessageBox.critical(self, "Download Failed", str(e))
    
    # ============================================================
    # DOWNLOAD FROM HISTORY
    # ============================================================

    def handle_history_download(self, item):
        """Handle download from history"""
        from api import download_report
        
        dataset_id = int(item.text().split()[1])
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report PDF",
            f"report_{dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if save_path:
            try:
                download_report(dataset_id, save_path)
            except Exception as e:
                QMessageBox.critical(self, "Download Failed", str(e))
    
    # ============================================================
    # LOGOUT
    # ============================================================

    def handle_logout(self):
        """Handle logout"""
        from api import logout
        
        logout()
        
        QMessageBox.information(
            self,
            "Logged Out ✅",
            "You have been logged out successfully."
        )
        
        self.reset()
        self.logout_requested.emit()
    
    # ============================================================
    # HISTORY
    # ============================================================

    def load_history(self):
        """Load upload history"""
        from api import get_history
        
        try:
            history_data = get_history()
            self.sidebar.load_history(history_data)
        except Exception as e:
            QMessageBox.critical(self, "Failed to load history", str(e))
    
    # ============================================================
    # RESET
    # ============================================================

    def reset(self):
        """Reset dashboard"""
        self.current_dataset_id = None
        self.sidebar.clear_history()
        self.sidebar.enable_download(False)
        self.content_area.reset_all()
    
    def initialize(self):
        """Initialize dashboard"""
        self.load_history()
