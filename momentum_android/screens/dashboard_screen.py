
"""
dashboard_screen.py
-------------------
Momentum mobile dashboard.

Displays greeting, statistics, today's habits, today's routine,
and weekly progress. Routine items can be completed directly
from the dashboard using the existing DashboardController.
"""

from __future__ import annotations

from kivy.app import App
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox

from controllers.dashboard_controller import DashboardController
from screens.base_screen import (
    StandardLayout,
    make_card,
    section_label,
    stat_card,
    progress_row,
)
from themes.theme import COLORS
from utils.logger import get_logger

log = get_logger("screens.dashboard_screen")


class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = DashboardController()
        self._layout: StandardLayout | None = None
        self._refreshing = False
        self._build()

    def _build(self) -> None:
        self._layout = StandardLayout(
            title="Momentum",
            current_tab="dashboard",
        )
        self.add_widget(self._layout)
        self._populate()

    def _populate(self) -> None:
        if self._refreshing:
            return

        self._refreshing = True
        try:
            self._render_dashboard()
        finally:
            self._refreshing = False

    def _render_dashboard(self) -> None:
        content = self._layout.content_area
        content.clear_widgets()

        try:
            summary = self.controller.get_summary()
        except Exception:
            log.exception("Failed to load dashboard summary")
            content.add_widget(
                MDLabel(
                    text="Could not load dashboard. Please try again.",
                    halign="center",
                    size_hint_y=None,
                    height=dp(48),
                )
            )
            return

        # Greeting
        greeting_card = make_card(
            padding=dp(16),
            size_hint_y=None,
            height=dp(88),
        )
        greeting_inner = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4),
        )
        greeting_inner.add_widget(
            MDLabel(
                text=summary.greeting,
                font_style="H6",
                theme_text_color="Custom",
                text_color=COLORS["text_primary"],
            )
        )
        greeting_inner.add_widget(
            MDLabel(
                text=summary.date_str,
                font_style="Caption",
                theme_text_color="Custom",
                text_color=COLORS["text_secondary"],
            )
        )
        greeting_card.add_widget(greeting_inner)
        content.add_widget(greeting_card)

        # Statistics
        self._add_stat_row(
            content,
            [
                (summary.xp_today, "XP Today", COLORS["accent"]),
                (f"Lv {summary.level}", "Level", COLORS["accent_alt"]),
                (str(summary.streak), "Streak", COLORS["warning"]),
            ],
        )
        self._add_stat_row(
            content,
            [
                (
                    summary.pomodoro_sessions,
                    "Pomodoros",
                    COLORS["secondary"],
                ),
                (
                    f"{summary.focus_minutes}m",
                    "Focus",
                    COLORS["secondary"],
                ),
                (
                    f"{summary.study_hours:.1f}h",
                    "Study",
                    COLORS["accent_alt"],
                ),
            ],
        )

        # Today's habits
        content.add_widget(section_label("Today's Habits"))

        habit_inner = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4),
        )
        habit_inner.bind(
            minimum_height=habit_inner.setter("height")
        )

        habit_done = summary.habits_completed
        habit_total = summary.habits_total

        habit_inner.add_widget(
            self._caption(f"{habit_done}/{habit_total} completed")
        )

        if habit_total:
            habit_inner.add_widget(
                progress_row(
                    habit_done / habit_total * 100,
                    COLORS["secondary"],
                    )
            )

        for habit in summary.habits[:6]:
            habit_id = habit["id"]
            completed = bool(habit["is_completed"])

            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(44),
                spacing=dp(8),
            )

            checkbox = MDCheckbox(
                active=completed,
                color_active=COLORS["secondary"],
                size_hint=(None, None),
                size=(dp(40), dp(40)),
            )
            checkbox.bind(
                active=lambda widget, active, hid=habit_id: (
                    self._toggle_habit(hid, widget, active)
                )
            )
            row.add_widget(checkbox)

            row.add_widget(
                MDLabel(
                    text=habit["name"],
                    theme_text_color="Custom",
                    text_color=(
                        COLORS["text_secondary"]
                        if completed
                        else COLORS["text_primary"]
                    ),
                    valign="middle",
                )
            )
            habit_inner.add_widget(row)

        if habit_total > 6:
            habit_inner.add_widget(
                MDFlatButton(
                    text=f"+ {habit_total - 6} more — go to Habits",
                    size_hint_y=None,
                    height=dp(44),
                    on_release=lambda *_: (
                        App.get_running_app().navigate("habits")
                    ),
                )
            )

        content.add_widget(self._content_card(habit_inner))

        # Daily routine
        content.add_widget(section_label("Daily Routine"))

        routine_inner = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
        )
        routine_inner.bind(
            minimum_height=routine_inner.setter("height")
        )

        routine_done = summary.routine_completed
        routine_total = summary.routine_total

        routine_inner.add_widget(
            self._caption(
                f"{routine_done}/{routine_total} completed"
            )
        )

        if routine_total:
            routine_inner.add_widget(
                progress_row(
                    routine_done / routine_total * 100,
                    COLORS["accent"],
                    )
            )

        for item in summary.routine_items[:5]:
            item_id = item["id"]
            completed = bool(item["is_completed"])

            item_row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(40),
                spacing=dp(10),
                padding=(0, dp(2), 0, dp(2)),
            )

            item_button = MDFlatButton(
                text="",
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                on_release=lambda _, iid=item_id, state=completed: (
                    self._toggle_routine_item(iid, state)
                ),
            )
            item_button.add_widget(
                MDIcon(
                    icon=(
                        "check-circle"
                        if completed
                        else "checkbox-blank-circle-outline"
                    ),
                    theme_text_color="Custom",
                    text_color=(
                        COLORS["secondary"]
                        if completed
                        else COLORS["text_secondary"]
                    ),
                )
            )

            item_row.add_widget(item_button)
            item_row.add_widget(
                MDLabel(
                    text=item["name"],
                    font_style="Body1",
                    theme_text_color="Custom",
                    text_color=(
                        COLORS["text_secondary"]
                        if completed
                        else COLORS["text_primary"]
                    ),
                    valign="middle",
                )
            )
            routine_inner.add_widget(item_row)

        if routine_total > 5:
            routine_inner.add_widget(
                MDFlatButton(
                    text=f"+ {routine_total - 5} more — go to Routine",
                    size_hint_y=None,
                    height=dp(44),
                    on_release=lambda *_: (
                        App.get_running_app().navigate("routine")
                    ),
                )
            )

        content.add_widget(self._content_card(routine_inner))

        # Weekly progress
        content.add_widget(section_label("Last 7 Days"))

        week_inner = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8),
        )
        week_inner.bind(
            minimum_height=week_inner.setter("height")
        )

        for day in summary.weekly_progress:
            percentage = (
                day["pct"] if day["total"] > 0 else 0
            )
            percentage = max(0, min(100, percentage))

            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(28),
                spacing=dp(8),
            )

            row.add_widget(
                MDLabel(
                    text=day["label"],
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=COLORS["text_secondary"],
                    size_hint=(None, 1),
                    width=dp(38),
                    valign="middle",
                )
            )
            row.add_widget(
                progress_row(percentage, COLORS["secondary"])
            )
            row.add_widget(
                MDLabel(
                    text=f"{int(percentage)}%",
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=COLORS["text_secondary"],
                    size_hint=(None, 1),
                    width=dp(40),
                    halign="right",
                    valign="middle",
                )
            )
            week_inner.add_widget(row)

        content.add_widget(self._content_card(week_inner))
        content.add_widget(
            MDBoxLayout(size_hint_y=None, height=dp(16))
        )

    @staticmethod
    def _caption(text: str) -> MDLabel:
        return MDLabel(
            text=text,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=COLORS["text_secondary"],
            size_hint_y=None,
            height=dp(24),
            valign="middle",
        )

    @staticmethod
    def _content_card(inner: MDBoxLayout):
        card = make_card(
            padding=dp(16),
            size_hint=(1, None),
        )
        card.add_widget(inner)

        def update_height(*_):
            card.height = inner.height + dp(32)

        inner.bind(height=update_height)
        update_height()
        return card

    @staticmethod
    def _add_stat_row(content, stats) -> None:
        row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(96),
            spacing=dp(8),
        )
        for value, label, color in stats:
            row.add_widget(stat_card(str(value), label, color))
        content.add_widget(row)

    def _toggle_habit(
            self,
            habit_id: int,
            widget,
            new_active: bool,
    ) -> None:
        try:
            self.controller.toggle_habit(
                habit_id,
                not new_active,
            )
        except Exception:
            log.exception("Failed to toggle habit %s", habit_id)
            widget.active = not new_active
            return

        self._populate()

    def _toggle_routine_item(
            self,
            item_id: int,
            current_state: bool,
    ) -> None:
        try:
            self.controller.toggle_routine_item(
                item_id,
                current_state,
            )
        except Exception:
            log.exception(
                "Failed to toggle routine item %s",
                item_id,
            )
            return

        self._populate()

    def on_enter(self, *_args) -> None:
        """Refresh dashboard data when the screen becomes active."""
        self._populate()
