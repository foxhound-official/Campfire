from app.theme.colors import Colors
from app.theme.radius import Radius


def load_stylesheet() -> str:
	return f"""
    QWidget {{
        background: {Colors.BACKGROUND};
        color: {Colors.TEXT};
    }}

    QFrame {{
        background: {Colors.PANEL};
        border: 1px solid {Colors.BORDER};
        border-radius: {Radius.MD}px;
    }}

    QLineEdit,
    QSpinBox,
    QListWidget {{
        background: {Colors.PANEL_LIGHT};
        border: 1px solid {Colors.BORDER};
        border-radius: {Radius.SM}px;
        padding: 4px;
    }}

    QProgressBar {{
        border: 1px solid {Colors.BORDER};
        border-radius: {Radius.SM}px;
        text-align: center;
    }}

    QProgressBar::chunk {{
        background: {Colors.ACCENT};
    }}
    """
