
"""
menu_screen.py
---------------
More hub screen — a list of cards that navigate to secondary screens.
Uses Material Design Icons instead of emoji glyphs.
Compatible with KivyMD 1.2.0.
"""

from __future__ import annotations

from kivy.app import App
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton

from screens.base_screen import StandardLayout
from themes.theme import COLORS, RADIUS


MENU_ENTRIES = [
    ("calendar-month", "Calendar", "Daily notes & mood", "calendar"),
    ("book-open-variant", "Study Tracker", "Log your study hours", "study"),
    ("chart-bar", "Statistics", "7-day productivity view", "statistics"),
    ("target", "Goals", "Track what matters", "goals"),
    ("folder-outline", "Projects", "Monitor progress", "projects"),
    ("timer-outline", "Focus Mode", "25-min deep work", "focus"),
    ("cog-outline", "Settings", "App info & backup", "settings"),
]


class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build()

    def _build(self) -> None:
        self._layout = StandardLayout(
            title="More",
            current_tab="menu",
        )
        self.add_widget(self._layout)

        content = self._layout.content_area
        content.add_widget(
            MDLabel(
                text="All Features",
                font_style="H6",
                theme_text_color="Custom",
                text_color=COLORS["text_primary"],
                size_hint_y=None,
                height=dp(40),
            )
        )

        for icon, title, subtitle, screen_name in MENU_ENTRIES:
            content.add_widget(
                self._menu_card(icon, title, subtitle, screen_name)
            )

        content.add_widget(
            MDBoxLayout(size_hint_y=None, height=dp(16))
        )

    def _menu_card(
            self,
            icon: str,
            title: str,
            subtitle: str,
            screen_name: str,
    ) -> MDCard:
        card = MDCard(
            orientation="horizontal",
            md_bg_color=COLORS["surface"],
            radius=[dp(RADIUS)],
            padding=dp(12),
            spacing=dp(12),
            line_color=COLORS["border"],
            line_width=1,
            size_hint=(1, None),
            height=dp(88),
            ripple_behavior=True,
        )

        # Icon column
        icon_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=dp(48),
        )
        icon_box.add_widget(
            MDIconButton(
                icon=icon,
                theme_icon_color="Custom",
                icon_color=COLORS["accent"],
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_release=lambda *_: self._navigate(screen_name),
            )
        )
        card.add_widget(icon_box)

        # Title and subtitle
        text_column = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2),
        )
        text_column.add_widget(
            MDLabel(
                text=title,
                font_style="Body1",
                theme_text_color="Custom",
                text_color=COLORS["text_primary"],
                size_hint_y=None,
                height=dp(28),
                valign="middle",
            )
        )
        text_column.add_widget(
            MDLabel(
                text=subtitle,
                font_style="Caption",
                theme_text_color="Custom",
                text_color=COLORS["text_secondary"],
                size_hint_y=None,
                height=dp(24),
                valign="middle",
            )
        )
        card.add_widget(text_column)

        # Chevron action
        card.add_widget(
            MDIconButton(
                icon="chevron-right",
                theme_icon_color="Custom",
                icon_color=COLORS["text_secondary"],
                size_hint=(None, None),
                size=(dp(36), dp(48)),
                on_release=lambda *_: self._navigate(screen_name),
            )
        )

        # KivyMD 1.2.0 MDCard is not a ButtonBehavior.
        # Bind its touch event without modifying its inheritance.
        card.bind(
            on_touch_up=lambda widget, touch: (
                self._navigate(screen_name)
                if widget.collide_point(*touch.pos)
                   and touch.grab_current is None
                   and touch.button is None
                   and not touch.is_mouse_scrolling
                else None
            )
        )

        return card

    @staticmethod
    def _navigate(screen_name: str) -> None:
        App.get_running_app().navigate(screen_name)
