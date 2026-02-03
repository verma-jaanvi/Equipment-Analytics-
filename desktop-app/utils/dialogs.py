"""
Dialog utility functions
"""

from PyQt5.QtWidgets import QMessageBox


def show_welcome(user):
    """
    Shows welcome popup after successful login
    
    Args:
        user (str): Username of logged in user
    """
    msg = QMessageBox()
    msg.setWindowTitle("Login Successful ✅")
    msg.setText(f"Welcome back, {user} 👋")
    msg.setInformativeText("You are now inside the Equipment Analytics Dashboard.")
    msg.setStyleSheet("""
        QMessageBox {
            background: white;
            font-family: Segoe UI;
            font-size: 15px;
        }
        QLabel {
            font-size: 16px;
            font-weight: 600;
            color: #0f172a;
        }
        QPushButton {
            padding: 10px;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-weight: 700;
        }
    """)
    msg.exec_()


def show_error(title, message):
    """
    Shows error dialog
    
    Args:
        title (str): Dialog title
        message (str): Error message
    """
    QMessageBox.critical(None, title, message)


def show_success(title, message):
    """
    Shows success dialog
    
    Args:
        title (str): Dialog title
        message (str): Success message
    """
    QMessageBox.information(None, title, message)


def show_warning(title, message):
    """
    Shows warning dialog
    
    Args:
        title (str): Dialog title
        message (str): Warning message
    """
    QMessageBox.warning(None, title, message)