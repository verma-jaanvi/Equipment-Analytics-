"""
Main Application - Chemical Equipment Visualizer
Entry point that assembles all components together
"""

from PyQt5.QtWidgets import QWidget, QStackedLayout

# ✅ Import stylesheet
from styles import GLOBAL_STYLESHEET

# ✅ Import UI pages properly from package
from components.login_page import LoginPage
from components.signup_page import SignupPage
from components.dashboard import Dashboard


class MainWindow(QWidget):
    """
    Main application window - orchestrates all pages
    """

    def __init__(self):
        super().__init__()

        # Window configuration
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1750, 960)

        # Apply global theme
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # Setup UI
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Setup stacked pages"""

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        # Pages
        self.login_page = LoginPage()
        self.signup_page = SignupPage()
        self.dashboard_page = Dashboard()

        # Add pages
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.signup_page)
        self.stack.addWidget(self.dashboard_page)

        # Default page
        self.stack.setCurrentWidget(self.login_page)

    def connect_signals(self):
        """Connect navigation signals"""

        # Login → Dashboard
        self.login_page.login_successful.connect(self.show_dashboard)

        # Login → Signup
        self.login_page.switch_to_signup.connect(self.show_signup)

        # Signup → Login
        self.signup_page.switch_to_login.connect(self.show_login)

        # Dashboard → Logout → Login
        self.dashboard_page.logout_requested.connect(self.show_login)

    def show_login(self):
        """Go back to login page"""
        self.login_page.clear_inputs()
        self.stack.setCurrentWidget(self.login_page)

    def show_signup(self):
        """Go to signup page"""
        self.signup_page.clear_inputs()
        self.stack.setCurrentWidget(self.signup_page)

    def show_dashboard(self):
        """Go to dashboard page"""
        self.dashboard_page.initialize()
        self.stack.setCurrentWidget(self.dashboard_page)