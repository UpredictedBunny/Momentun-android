
"""
base_screen.py
--------------
Shared base for every Momentum Android screen.
"""

from __future__ import annotations

from typing import Callable

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.toolbar import MDTopAppBar

from themes.theme import COLORS, PAD, FONT_SIZE, RADIUS


BOTTOM_NAV_ITEMS = [
    ("home", "dashboard", "Home"),
    ("checkbox-marked-circle", "habits", "Habits"),
    ("weather-sunny", "routine", "Routine"),
    ("timer", "pomodoro", "Pomodoro"),
    ("dots-grid", "menu", "More"),
]


class BottomNavBar(MDBoxLayout):
    """Persistent bottom navigation bar."""

    def __init__(self, current: str = "dashboard", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(60)
        self.md_bg_color = COLORS["surface"]

        for icon, screen_name, label in BOTTOM_NAV_ITEMS:
            is_active = screen_name == current
            color = (
                COLORS["accent"]
                if is_active
                else COLORS["text_secondary"]
            )

            button = MDIconButton(
                icon=icon,
                theme_icon_color="Custom",
                icon_color=color,
                size_hint=(1, None),
                height=dp(60),
                on_release=lambda _, name=screen_name: (
                    App.get_running_app().navigate(name)
                ),
            )
            self.add_widget(button)


class StandardLayout(MDBoxLayout):
    """Root layout with toolbar, scrollable content and bottom navigation."""

    def __init__(
            self,
            title: str = "Momentum",
            current_tab: str = "dashboard",
            right_icons: list | None = None,
            **kwargs,
    ):
        super().__init__(
            orientation="vertical",
            **kwargs,
        )
        self.md_bg_color = COLORS["background"]

        self.toolbar = MDTopAppBar(
            title=title,
            md_bg_color=COLORS["surface"],
            specific_text_color=COLORS["text_primary"],
            right_action_items=right_icons or [],
        )
        self.add_widget(self.toolbar)

        self.scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(3),
            scroll_type=["content", "bars"],
        )

        self.content_area = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=0,
            padding=[
                dp(PAD["md"]),
                dp(PAD["sm"]),
            ],
            spacing=dp(PAD["sm"]),
        )
        self.content_area.bind(
            minimum_height=self.content_area.setter("height")
        )

        self.scroll.add_widget(self.content_area)
        self.add_widget(self.scroll)

        self.add_widget(BottomNavBar(current=current_tab))


def make_card(padding: int = 16, **kwargs) -> MDCard:
    """Create a consistently styled surface card."""

    kwargs.setdefault("size_hint_x", 1)

    card = MDCard(
        md_bg_color=COLORS["surface"],
        radius=[dp(RADIUS)],
        padding=dp(padding),
        line_color=COLORS["border"],
        line_width=1,
        **kwargs,
    )
    return card


def section_label(text: str) -> MDLabel:
    """Small section heading."""

    return MDLabel(
        text=text.upper(),
        font_style="Caption",
        theme_text_color="Custom",
        text_color=COLORS["text_secondary"],
        size_hint_y=None,
        height=dp(28),
    )


def show_dialog(
        title: str,
        text: str,
        ok_text: str = "OK",
) -> None:
    """Display an informational dialog."""

    dialog = None

    def dismiss_dialog(*_):
        if dialog is not None:
            dialog.dismiss()

    dialog = MDDialog(
        title=title,
        text=text,
        buttons=[
            MDFlatButton(
                text=ok_text,
                on_release=dismiss_dialog,
            )
        ],
    )
    dialog.open()


def show_confirm(
        title: str,
        text: str,
        on_confirm: Callable,
        confirm_text: str = "CONFIRM",
        cancel_text: str = "CANCEL",
) -> None:
    """Display a destructive-action confirmation dialog."""

    dialog = None

    def cancel(*_):
        if dialog is not None:
            dialog.dismiss()

    def confirm(*_):
        if dialog is not None:
            dialog.dismiss()
        on_confirm()

    dialog = MDDialog(
        title=title,
        text=text,
        buttons=[
            MDFlatButton(
                text=cancel_text,
                on_release=cancel,
            ),
            MDRaisedButton(
                text=confirm_text,
                md_bg_color=COLORS["danger"],
                on_release=confirm,
            ),
        ],
    )
    dialog.open()


def stat_card(
        value: str,
        label: str,
        color: list | None = None,
) -> MDCard:
    """Display a statistic and its caption."""

    card = make_card(
        padding=dp(12),
        size_hint=(1, None),
        height=dp(90),
    )

    inner = MDBoxLayout(
        orientation="vertical",
        spacing=dp(2),
    )

    inner.add_widget(
        MDLabel(
            text=str(value),
            font_style="H5",
            theme_text_color="Custom",
            text_color=color or COLORS["accent"],
            halign="center",
            valign="middle",
        )
    )

    inner.add_widget(
        MDLabel(
            text=label,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=COLORS["text_secondary"],
            halign="center",
            valign="middle",
        )
    )

    card.add_widget(inner)
    return card


def progress_row(
        value: float,
        color: list | None = None,
) -> MDProgressBar:
    """Create a compact progress bar."""

    return MDProgressBar(
        value=max(0, min(100, value)),
        color=color or COLORS["accent"],
        size_hint_y=None,
        height=dp(6),
    )
