"""
Login page component
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal


class LoginPage(QWidget):
    """
    Login page component
    """
    
    # Signals
    login_successful = pyqtSignal()
    switch_to_signup = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login page UI"""
        from styles import modern_card
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Login Card
        card = modern_card()
        card.setFixedWidth(600)

        form = QVBoxLayout()
        form.setSpacing(22)

        # Avatar (centered)
        avatar = QLabel("👤")
        avatar.setStyleSheet("""
            font-size: 55px;
            background: #2563eb;
            color: white;
            padding: 20px;
            border-radius: 55px;
            min-width: 95px;
            min-height: 95px;
        """)

        avatar_row = QHBoxLayout()
        avatar_row.addStretch()
        avatar_row.addWidget(avatar)
        avatar_row.addStretch()

        # Title
        title = QLabel("LOGIN")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: 900;
            color: #2563eb;
        """)

        # Input fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)

        # Login button
        login_btn = QPushButton("LOGIN")
        login_btn.clicked.connect(self.handle_login)

        # Register link
        register_link = QPushButton("Register")
        register_link.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2563eb;
                font-size: 15px;
                font-weight: 700;
            }
        """)
        register_link.clicked.connect(self.switch_to_signup.emit)

        # Assemble form
        form.addLayout(avatar_row)
        form.addWidget(title)
        form.addWidget(self.username_input)
        form.addWidget(self.password_input)
        form.addWidget(login_btn)
        form.addWidget(register_link)

        card.setLayout(form)
        layout.addWidget(card)
    
    def handle_login(self):
        """Handle login button click"""
        from api import login
        from utils import show_welcome
        from PyQt5.QtWidgets import QMessageBox
        
        try:
            username = self.username_input.text()
            password = self.password_input.text()

            login(username, password)
            show_welcome(username)
            self.login_successful.emit()

        except:
            QMessageBox.critical(self, "Login Failed", "Invalid credentials!")
    
    def clear_inputs(self):
        """Clear input fields"""
        self.username_input.clear()
        self.password_input.clear()