"""
Signup page component
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal


class SignupPage(QWidget):
    """
    Signup/Registration page component
    """
    
    # Signal to switch back to login page
    switch_to_login = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the signup page UI"""
        from styles import modern_card
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = modern_card()
        card.setFixedWidth(620)

        form = QVBoxLayout()
        form.setSpacing(22)

        # Title
        title = QLabel("SIGN UP")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 34px;
            font-weight: 900;
            color: #2563eb;
        """)

        # Input fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("New Username")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email Address")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("New Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_signup)

        # Signup button
        signup_btn = QPushButton("CREATE ACCOUNT")
        signup_btn.clicked.connect(self.handle_signup)

        # Back to login button
        back_btn = QPushButton("Back to Login")
        back_btn.setStyleSheet("""
            background: transparent;
            color: #2563eb;
            font-weight: 700;
        """)
        back_btn.clicked.connect(self.switch_to_login.emit)

        # Assemble form
        form.addWidget(title)
        form.addWidget(self.username_input)
        form.addWidget(self.email_input)
        form.addWidget(self.password_input)
        form.addWidget(signup_btn)
        form.addWidget(back_btn)

        card.setLayout(form)
        layout.addWidget(card)
    
    def handle_signup(self):
        """Handle signup button click"""
        from api import signup
        
        try:
            username = self.username_input.text()
            email = self.email_input.text()
            password = self.password_input.text()

            if not username or not email or not password:
                QMessageBox.warning(
                    self,
                    "Missing Fields",
                    "Please fill all fields before signing up."
                )
                return

            signup(username, email, password)

            QMessageBox.information(
                self,
                "Signup Successful ✅",
                "Account created successfully!\nNow login to continue."
            )

            self.clear_inputs()
            self.switch_to_login.emit()

        except Exception as e:
            QMessageBox.critical(self, "Signup Failed ❌", str(e))
    
    def clear_inputs(self):
        """Clear input fields"""
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()