from app.theme.gm_colors import GMColors
from app.theme.radius import Radius


def load_gm_stylesheet() -> str:
	return f"""
	QWidget {{
		background: transparent;
		color: {GMColors.TEXT};
		font-size: 13px;
	}}

	QMainWindow {{
		background: {GMColors.BACKGROUND};
	}}

	QFrame#gmToolbar,
	QFrame#gmPanel {{
		background: {GMColors.PANEL};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
	}}

	QLabel#gmAppTitle {{
		color: {GMColors.TEXT};
		font-size: 17px;
		font-weight: 700;
	}}

	QLabel#gmSceneName {{
		color: {GMColors.TEXT_MUTED};
	}}

	QLabel#gmPanelTitle {{
		color: {GMColors.TEXT};
		font-size: 14px;
		font-weight: 700;
	}}

	QLabel#gmPlaceholder {{
		color: {GMColors.TEXT_MUTED};
	}}

	QPushButton {{
		background: {GMColors.PANEL_ALT};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
		color: {GMColors.TEXT};
		padding: 7px 12px;
	}}

	QPushButton:hover {{
		background: {GMColors.SURFACE};
		border-color: {GMColors.BORDER_LIGHT};
	}}

	QPushButton:pressed {{
		background: {GMColors.BACKGROUND};
	}}

	QPushButton#gmPrimaryButton {{
		background: {GMColors.ACCENT};
		border-color: {GMColors.ACCENT};
		color: {GMColors.BACKGROUND};
		font-weight: 700;
	}}

	QPushButton#gmPrimaryButton:hover {{
		background: {GMColors.ACCENT_HOVER};
	}}

	QTabWidget#gmMainTabs::pane {{
		background: transparent;
		border: none;
	}}

	QTabWidget#gmMainTabs QTabBar::tab {{
		background: {GMColors.PANEL};
		border: 1px solid {GMColors.BORDER};
		color: {GMColors.TEXT_MUTED};
		min-width: 130px;
		padding: 10px 18px;
	}}

	QTabWidget#gmMainTabs QTabBar::tab:selected {{
		background: {GMColors.PANEL_ALT};
		border-bottom: 2px solid {GMColors.ACCENT};
		color: {GMColors.TEXT};
	}}

	QTabWidget#gmMainTabs QTabBar::tab:hover {{
		color: {GMColors.TEXT};
	}}

	QTabWidget#gmBottomTabs::pane {{
		background: {GMColors.PANEL};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
	}}

	QTabWidget#gmBottomTabs QTabBar::tab {{
		background: {GMColors.BACKGROUND};
		border: 1px solid {GMColors.BORDER};
		color: {GMColors.TEXT_MUTED};
		padding: 7px 14px;
	}}

	QTabWidget#gmBottomTabs QTabBar::tab:selected {{
		background: {GMColors.PANEL};
		border-top: 2px solid {GMColors.ACCENT};
		color: {GMColors.TEXT};
	}}

	QSplitter::handle {{
		background: {GMColors.BORDER};
	}}

	QSplitter::handle:horizontal {{
		width: 2px;
	}}

	QSplitter::handle:vertical {{
		height: 2px;
	}}

	QSplitter::handle:hover {{
		background: {GMColors.ACCENT};
	}}
	
		QScrollArea#gmCharacterScroll,
	QWidget#gmCharacterList {{
		background: transparent;
		border: none;
	}}

	QFrame#gmCharacterCard {{
		background: {GMColors.PANEL_ALT};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
	}}

	QFrame#gmCharacterCard:hover {{
		background: {GMColors.SURFACE};
		border-color: {GMColors.BORDER_LIGHT};
	}}

	QFrame#gmCharacterCard[selected="true"] {{
		background: {GMColors.SELECTION};
		border-color: {GMColors.ACCENT};
	}}
	
		QLabel#gmCharacterPortrait,
	QLabel#gmInspectorPortrait {{
		background: {GMColors.BACKGROUND};
		border: 1px solid {GMColors.BORDER_LIGHT};
		border-radius: {Radius.SM}px;
		color: {GMColors.TEXT_MUTED};
		font-size: 18px;
		font-weight: 700;
	}}

	QLabel#gmCharacterName {{
		font-size: 14px;
		font-weight: 700;
	}}

	QLabel#gmCharacterMeta,
	QLabel#gmInspectorCaption {{
		color: {GMColors.TEXT_MUTED};
	}}

	QLabel#gmConnectionOffline {{
		color: {GMColors.TEXT_MUTED};
		font-size: 11px;
	}}

	QLabel#gmConnectionOnline {{
		color: {GMColors.SUCCESS};
		font-size: 11px;
	}}

	QProgressBar#gmCharacterHealth,
	QProgressBar#gmInspectorHealth {{
		background: {GMColors.BACKGROUND};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
		color: {GMColors.TEXT};
		font-size: 11px;
		font-weight: 600;
		text-align: center;
	}}

	QProgressBar#gmCharacterHealth {{
		min-height: 16px;
		max-height: 16px;
	}}

	QProgressBar#gmInspectorHealth {{
		min-height: 20px;
		max-height: 20px;
	}}

	QProgressBar#gmCharacterHealth::chunk,
	QProgressBar#gmInspectorHealth::chunk {{
		background: {GMColors.DANGER};
		border-radius: {Radius.SM}px;
	}}

	QLabel#gmInspectorName {{
		font-size: 20px;
		font-weight: 700;
	}}

	QLabel#gmLevelBadge {{
		background: {GMColors.ACCENT};
		border-radius: {Radius.SM}px;
		color: {GMColors.BACKGROUND};
		font-size: 12px;
		font-weight: 700;
		padding: 4px 7px;
	}}

	QFrame#gmInspectorSection {{
		background: {GMColors.PANEL_ALT};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
	}}

	QLabel#gmInspectorValue {{
		font-weight: 600;
	}}
	
		QScrollArea#gmInspectorScroll {{
		background: transparent;
		border: none;
	}}

	QLabel#gmInspectorSectionTitle {{
		font-size: 13px;
		font-weight: 700;
	}}

	QFrame#gmFeatureItem {{
		background: {GMColors.BACKGROUND};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
	}}

	QLabel#gmFeatureTitle {{
		font-weight: 700;
	}}

	QLabel#gmFeatureDescription {{
		color: {GMColors.TEXT_MUTED};
		font-size: 12px;
	}}
	
		QComboBox#gmSceneSelector {{
		background: {GMColors.PANEL_ALT};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
		color: {GMColors.TEXT};
		padding: 7px 10px;
	}}

	QComboBox#gmSceneSelector:hover {{
		border-color: {GMColors.BORDER_LIGHT};
	}}

	QComboBox#gmSceneSelector QAbstractItemView {{
		background: {GMColors.PANEL_ALT};
		border: 1px solid {GMColors.BORDER};
		color: {GMColors.TEXT};
		selection-background-color: {GMColors.SELECTION};
	}}

	QLabel#gmScenePreviewTitle {{
		font-size: 20px;
		font-weight: 700;
	}}

	QLabel#gmSceneTypeBadge {{
		color: {GMColors.ACCENT};
		font-size: 12px;
		font-weight: 700;
	}}

	QLabel#gmSceneDescription {{
		background: {GMColors.PANEL_ALT};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
		padding: 12px;
	}}

	QLabel#gmSceneResource {{
		color: {GMColors.TEXT_MUTED};
	}}
	
		QScrollArea#gmCreatureScroll,
	QWidget#gmCreatureList {{
		background: transparent;
		border: none;
	}}

	QFrame#gmCreatureCard {{
		background: {GMColors.PANEL_ALT};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
	}}

	QLabel#gmCreaturePortrait {{
		background: {GMColors.BACKGROUND};
		border: 1px solid {GMColors.BORDER_LIGHT};
		border-radius: {Radius.SM}px;
		color: {GMColors.TEXT_MUTED};
		font-size: 18px;
		font-weight: 700;
	}}

	QLabel#gmCreatureName {{
		font-weight: 700;
	}}

	QProgressBar#gmCreatureHealth {{
		background: {GMColors.BACKGROUND};
		border: 1px solid {GMColors.BORDER};
		border-radius: {Radius.SM}px;
		color: {GMColors.TEXT};
		font-size: 11px;
		font-weight: 600;
		min-height: 16px;
		max-height: 16px;
		text-align: center;
	}}

	QProgressBar#gmCreatureHealth::chunk {{
		background: {GMColors.DANGER};
		border-radius: {Radius.SM}px;
	}}
	
	"""