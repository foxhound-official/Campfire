from app.theme.colors import Colors
from app.theme.images import ASSETS_PATH
from app.theme.radius import Radius


def load_stylesheet() -> str:
	parchment_texture = (
			ASSETS_PATH
			/ "textures"
			/ "texture_parchment.png"
	).as_posix()
	leather_texture = (
			ASSETS_PATH
			/ "textures"
			/ "texture_leather.png"
	).as_posix()
	inventory_backpack_texture = (
			ASSETS_PATH
			/ "textures"
			/ "texture_inventory_backpack.png"
	).as_posix()
	inventory_handle_texture = (
			ASSETS_PATH
			/ "textures"
			/ "texture_inventory_handle.png"
	).as_posix()

	return f"""

	QWidget {{
		background: transparent;
		color: {Colors.TEXT};
	}}

	QMainWindow {{
		background-color: {Colors.BACKGROUND};
		background-image: url("{leather_texture}");
		background-repeat: repeat-xy;
		background-position: top left;
	}}

	QFrame {{
		background: transparent;
		border: none;
	}}

	QFrame#characterPanel {{
		background-color: {Colors.PANEL};
		background-image: url("{parchment_texture}");
		background-repeat: repeat-xy;
		background-position: top left;

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
		background: {Colors.BACKGROUND_LIGHT};
		color: {Colors.TEXT_ON_DARK};
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
		background: {Colors.OVERLAY};
		color: {Colors.TEXT_ON_DARK};
	
		border: 1px solid {Colors.BORDER_LIGHT};
		border-radius: {Radius.MD}px;
	
		padding: 8px;
	
		font-weight: bold;
		font-size: 18px;
	}}
    
	QFrame#card {{
		background: {Colors.PANEL_LIGHT};
		border: 1px solid {Colors.BORDER};
		border-radius: {Radius.MD}px;
	}}
	
	QFrame#card:hover {{
		border-color: {Colors.ACCENT_HOVER};
	}}
	
	QLabel#cardImage {{
		background: {Colors.PANEL_DARK};
		border: none;
		border-radius: {Radius.SM}px;
	}}
	
	QLabel#cardTitle {{
		background: transparent;
		border: none;
		color: {Colors.TEXT};
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
		background: {Colors.BORDER};
		color: {Colors.TEXT_ON_DARK};
		border: 1px solid {Colors.BORDER_LIGHT};
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
		background: transparent;

		border-style: solid;
		border-width: 28px 20px 28px 20px;
		border-image: url("{inventory_backpack_texture}")
			78 74 78 74
			stretch stretch;

		border-radius: 0;
	}}

	QLabel#inventoryTitle {{
		background: transparent;
		border: none;
		color: {Colors.TEXT_ON_DARK};
		font-size: 18px;
		font-weight: 700;
	}}

	QLabel#inventoryCapacity {{
		background: transparent;
		border: none;
		color: {Colors.PANEL_DARK};
	}}

	QLabel#cardDescription,
	QLabel#itemQuantity {{
		background: transparent;
		border: none;
		color: {Colors.TEXT_SECONDARY};
	}}

	QPushButton#inventoryHandle {{
		background: transparent;

		border-style: solid;
		border-width: 8px 6px 8px 6px;
		border-image: url("{inventory_handle_texture}")
			32 28 32 28
			stretch stretch;

		color: {Colors.TEXT_ON_DARK};
		padding: 0;

		font-size: 24px;
		font-weight: 600;
	}}

	QPushButton#inventoryHandle:hover {{
		color: {Colors.ACCENT_HOVER};
	}}

	QPushButton#inventoryHandle:pressed {{
		padding-left: 1px;
	}}

    QScrollBar:vertical {{
    	background: transparent;
    	width: 10px;
    	margin: 0;
    }}

    QScrollBar::handle:vertical {{
    	background: {Colors.BORDER_LIGHT};
    	border-radius: {Radius.SM}px;
    	min-height: 28px;
    	margin: 2px;
    }}

    QScrollBar::handle:vertical:hover {{
    	background: {Colors.ACCENT};
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
    	background: transparent;
    	border: none;
    	height: 0;
    }}

    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
    	background: transparent;
    }}

    QLabel#sectionTitle {{
    	background: transparent;
    	color: {Colors.TEXT_SECONDARY};
    	border: none;
    	border-bottom: 1px solid {Colors.BORDER_LIGHT};
    	padding-bottom: 4px;
    	font-size: 11px;
    	font-weight: 700;
    }}

	QLabel#narrationText {{
		background: rgba(30, 20, 14, 215);
		border: 1px solid rgba(188, 146, 86, 180);
		border-radius: {Radius.LG}px;

		color: {Colors.TEXT_ON_DARK};
		padding: 24px 32px;

		font-size: 16px;
		font-weight: 500;
	}}

    """
