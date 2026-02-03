"""
Card styling functions
"""

from PyQt5.QtWidgets import QFrame


def modern_card():
    """
    Creates a modern styled card frame
    
    Returns:
        QFrame: Styled card frame
    """
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background: white;
            border-radius: 22px;
            padding: 35px;
            border: 1px solid rgba(0,0,0,0.07);
        }
    """)
    return card