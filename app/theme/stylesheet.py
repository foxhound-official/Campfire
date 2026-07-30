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
    
    QLabel#sceneBackground {{
    border: none;
    }}
    
    QLabel#sceneBanner {{
    background: rgba(25, 25, 25, 180);

    border: 1px solid #4A4B50;
    border-radius: 8px;

    padding: 8px;

    font-weight: bold;
    font-size: 18px;
    }}
    
    QFrame#card {{
    background: #2A2B2F;
    border: 1px solid #4A4B50;
    border-radius: 8px;
    }}
    
    QFrame#card:hover {{
    border: 1px solid #E09F3E;
    }}
    
    QLabel#cardImage {{
    background: #3A3B40;
    border-radius: 6px;
    border: none;
    }}

    QLabel#cardTitle {{
        background: transparent;
        border: none;
        font-weight: bold;
    }}

    QProgressBar#cardHealth {{
        min-height: 18px;
        max-height: 18px;
    }}

    QProgressBar#cardHealth::chunk {{
        background: {Colors.DANGER};
    }}

	QLabel#characterPortrait {{
		background: {Colors.BACKGROUND};
		border: 1px solid {Colors.BORDER};
		border-radius: {Radius.MD}px;
	}}
	
	QLabel#characterName {{
		background: transparent;
		border: none;
		font-size: 20px;
		font-weight: 700;
		padding-bottom: 4px;
	}}
	
	QLabel#identityCaption {{
		background: transparent;
		border: none;
		font-size: 11px;
	}}
	
	QLabel#identityValue {{
		background: transparent;
		border: none;
		font-size: 14px;
		font-weight: 600;
	}}
	
	QLabel#levelBadge,
	QLabel#temporaryHealth {{
		background: {Colors.BACKGROUND};
		border: 1px solid {Colors.BORDER};
		border-radius: {Radius.MD}px;
		font-weight: 600;
	}}
	
	QLabel#temporaryHealth {{
		padding: 2px 6px;
	}}
	
    QProgressBar#characterHealth {{
        min-height: 18px;
        max-height: 18px;
        border-radius: {Radius.SM}px;
        font-size: 11px;
    }}

    QFrame#statCell {{
        background: {Colors.PANEL_LIGHT};
        border: 1px solid {Colors.BORDER};
        border-radius: {Radius.SM}px;
    }}

    QLabel#statName {{
        background: transparent;
        border: none;
        color: {Colors.TEXT_SECONDARY};
        font-size: 10px;
        font-weight: 600;
    }}

    QLabel#statValue {{
        background: transparent;
        border: none;
        color: {Colors.TEXT};
        font-size: 16px;
        font-weight: 700;
    }}

    QTreeWidget#characterSkills {{
        background: {Colors.PANEL_LIGHT};
        border: 1px solid {Colors.BORDER};
        border-radius: {Radius.SM}px;
        outline: none;
    }}

    QTreeWidget#characterSkills::item {{
        background: transparent;
        border-bottom: 1px solid {Colors.BORDER};
        padding: 5px 4px;
    }}

    QTreeWidget#characterSkills::item:hover {{
        background: {Colors.PANEL};
    }}

    QTreeWidget#characterSkills::branch {{
        background: transparent;
    }}

    QListWidget#characterFeatures {{
        background: transparent;
        border: none;
        padding: 0;
        outline: none;
    }}

    QListWidget#characterFeatures::item {{
        background: {Colors.PANEL_LIGHT};
        border: 1px solid {Colors.BORDER};
        border-radius: {Radius.SM}px;
        padding: 7px 8px;
    }}

    QListWidget#characterFeatures::item:hover {{
        border-color: {Colors.ACCENT};
    }}

    QListWidget#characterFeatures::item:disabled {{
        background: transparent;
        border: none;
        color: {Colors.TEXT_SECONDARY};
    }}

    QWidget#characterParty,
    QWidget#partyMember {{
        background: transparent;
        border: none;
    }}

    QLabel#partyMemberPortrait {{
        background: {Colors.PANEL_LIGHT};
        border: 1px solid {Colors.BORDER};
        border-radius: {Radius.SM}px;
        color: {Colors.TEXT_SECONDARY};
        font-size: 14px;
        font-weight: 700;
    }}

    QProgressBar#partyMemberHealth {{
        min-height: 4px;
        max-height: 4px;
        background: {Colors.BACKGROUND};
        border: none;
        border-radius: 2px;
    }}

    QProgressBar#partyMemberHealth::chunk {{
        background: {Colors.DANGER};
        border-radius: 2px;
    }}

	QFrame#inventoryPanel {{
		background: transparent;
		border: none;
		border-radius: 0;
	}}

	QFrame#inventoryContent {{
		background: {Colors.PANEL};
		border: 1px solid {Colors.BORDER};
		border-radius: {Radius.MD}px;
	}}

	QPushButton#inventoryHandle {{
		background: {Colors.PANEL};
		border: 1px solid {Colors.BORDER};
		border-radius: {Radius.MD};
	}}

    """
