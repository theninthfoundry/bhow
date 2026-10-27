"""Bhow v0.2 — Python/Flet care journal wired to the real FastAPI service.

Preview release: no simulated care results, no fake clinic locations, no
AI-generated photos, and no diagnostic or dietary prescriptions.
"""
from datetime import date, datetime
from uuid import uuid4

import flet as ft

from api_client import Api, ApiError
from components import caption, heading, kicker, panel, primary, quiet, rule
from controller import CareController
from tokens import COLORS
from view_models import event_source, friendly_date, historical_date, next_action, safe_ingredient_status

TABS = ("Today", "Passport", "Check", "Explore")


def main(page: ft.Page) -> None:
    page.title = "Bhow · Care for their whole story"
    page.bgcolor = COLORS.paper
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    try:
        state = CareController(Api())
        state.load()
    except (RuntimeError, ApiError) as exc:
        page.add(
            ft.SafeArea(
                content=panel(
                    kicker("BHOW / CONNECTION"),
                    heading("Let's get you connected."),
                    caption(str(exc)),
                    caption("Start the FastAPI service. Local demo access requires explicit opt-in."),
                )
            )
        )
        return

    tab_index = 0
    message = ""
    passport_cache: dict[str, dict[str, object]] = {}

    def set_message(value: str) -> None:
        nonlocal message
        message = value

    def do(action, success: str = "") -> bool:
        try:
            action()
            set_message(success)
            return True
        except (ApiError, ValueError, RuntimeError) as exc:
            set_message(str(exc))
            return False

    def emergency(_=None) -> None:
        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Need urgent veterinary help?"),
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text(
                            "Difficulty breathing, collapse, suspected poisoning, "
                            "seizures or severe heat illness may require emergency care."
                        ),
                        ft.Text("Contact an emergency veterinary clinic immediately."),
                        ft.Text(
                            "Bhow does not currently have a verified live emergency "
                            "directory or provide a diagnosis.",
                            color=COLORS.muted,
                            size=12,
                        ),
                    ],
                ),
                actions=[ft.TextButton("Close", on_click=lambda _: page.pop_dialog())],
            )
        )

    def top_bar() -> ft.Control:
        options = [ft.DropdownOption(key=d["id"], text=d["name"]) for d in state.dogs]

        def selected(e) -> None:
            if do(lambda: state.choose(e.control.value)):
                render()
            else:
                render()

        return ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("BHOW.", size=21, weight=ft.FontWeight.BOLD, color=COLORS.ink),
                        quiet("HELP NOW", emergency),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Dropdown(
                                label="Caring for",
                                value=state.selected_id,
                                options=options,
                                on_select=selected,
                            ),
                        ),
                        quiet("+ Add dog", lambda _: open_new_dog()),
                    ]
                ),
                rule(),
            ],
        )

    def open_new_dog() -> None:
        dog_name = ft.TextField(label="Dog's name", max_length=80, autofocus=True)
        care_type = ft.Dropdown(
            label="Care relationship",
            value="owned",
            options=[
                ft.DropdownOption(key="owned", text="My dog"),
                ft.DropdownOption(key="foster", text="Foster dog"),
                ft.DropdownOption(key="community", text="Community dog"),
            ],
        )
        form_error = ft.Text("", color=COLORS.danger, size=12)

        def submit(_):
            if do(lambda: state.create(dog_name.value or "", care_type.value or "owned"), "Profile created"):
                passport_cache.clear()
                page.pop_dialog()
                render()
            else:
                form_error.value = message
                page.update()

        page.show_dialog(
            ft.BottomSheet(
                content=ft.Container(
                    padding=24,
                    content=ft.Column(
                        tight=True,
                        spacing=14,
                        controls=[
                            kicker("01 / FIRST INTRODUCTIONS"),
                            heading("Who are we caring for?", 28),
                            caption("Start with a name. Everything else can come later."),
                            dog_name,
                            care_type,
                            form_error,
                            primary("Create dog passport", submit, accent=True),
                            quiet("Not now", lambda _: page.pop_dialog()),
                        ],
                    ),
                ),
                scrollable=True,
                show_drag_handle=True,
            )
        )

    def open_task_form() -> None:
        if not state.selected_id:
            return
        dog_id = state.selected_id
        request_key = str(uuid4())
        title = ft.TextField(label="What needs doing?", max_length=140)
        kind = ft.Dropdown(
            label="Type", value="appointment",
            options=[ft.DropdownOption(key=k, text=k.replace("_", " ").title()) for k in
                     ("appointment", "vaccination", "parasite_prevention", "grooming", "other")],
        )
        due = {"date": date.today()}
        due_label = ft.Text(f"Due on {due['date'].strftime('%d %B %Y')}", color=COLORS.muted)
        form_error = ft.Text("", color=COLORS.danger, size=12)

        def choose_date(_):
            def pick(e):
                if e.control.value:
                    due["date"] = e.control.value.date()
                    due_label.value = f"Due on {due['date'].strftime('%d %B %Y')}"
                    page.update()

            page.show_dialog(ft.DatePicker(current_date=datetime.combine(due["date"], datetime.min.time()), on_change=pick))

        def submit(_):
            if do(
                lambda: state.api.add_task(
                    dog_id, kind.value or "other", (title.value or "").strip(), due["date"].isoformat(), key=request_key
                ),
                "Care reminder added",
            ):
                passport_cache.pop(dog_id, None)
                page.pop_dialog()
                render()
            else:
                form_error.value = message
                page.update()

        page.show_dialog(
            ft.BottomSheet(
                scrollable=True,
                show_drag_handle=True,
                content=ft.Container(padding=24, content=ft.Column(
                    tight=True, spacing=12,
                    controls=[
                        kicker("NEXT SMALL STEP"), heading("Plan some care.", 28),
                        caption("These are your own reminders, not vet-prescribed schedules."),
                        title, kind, due_label, quiet("Choose due date", choose_date),
                        form_error, primary("Save reminder", submit, accent=True),
                    ],
                )),
            )
        )

    def open_event_form() -> None:
        if not state.selected_id:
            return
        dog_id = state.selected_id
        request_key = str(uuid4())
        kind = ft.Dropdown(
            label="What happened?", value="other",
            options=[ft.DropdownOption(key=k, text=k.title()) for k in
                     ("weight", "vaccination", "visit", "symptom", "nutrition", "milestone", "other")],
        )
        notes = ft.TextField(label="Record your observation", multiline=True, min_lines=3, max_length=3000)
        date_value = date.today().isoformat()
        form_error = ft.Text("", size=12, color=COLORS.danger)

        def submit(_):
            if not (notes.value or "").strip():
                form_error.value = "Write a short observation before saving."
                page.update()
                return
            if do(
                lambda: state.api.add_event(dog_id, kind.value or "other", notes.value.strip(), date_value, key=request_key),
                "Caregiver observation saved",
            ):
                passport_cache.pop(dog_id, None)
                page.pop_dialog()
                render()
            else:
                form_error.value = message
                page.update()

        page.show_dialog(
            ft.BottomSheet(
                scrollable=True, show_drag_handle=True,
                content=ft.Container(padding=24, content=ft.Column(
                    tight=True, spacing=12,
                    controls=[
                        kicker("FIELD NOTE"), heading("What did you notice?", 28),
                        caption(f"Recorded for {date_value} · caregiver entry, not vet verified"),
                        kind, notes, form_error, primary("Save care note", submit, accent=True),
                    ],
                )),
            )
        )

    def task_row(task: dict) -> ft.Control:
        overdue = task["due_on"] < date.today().isoformat() and task["status"] == "pending"
        date_text = friendly_date(task["due_on"])

        def mark_complete(_):
            if do(
                lambda: state.api.complete_task(state.selected_id, task["id"]),
                "Reminder marked complete",
            ):
                render()
            else:
                render()

        return panel(
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        expand=True, spacing=5,
                        controls=[
                            kicker(task["kind"].replace("_", " ")),
                            ft.Text(task["title"], size=17, weight=ft.FontWeight.BOLD, color=COLORS.ink),
                            ft.Text(date_text, size=12, color=COLORS.danger if overdue else COLORS.muted),
                        ],
                    ),
                    quiet("Done" if task["status"] == "pending" else "✓", mark_complete)
                    if task["status"] == "pending" else caption("Completed"),
                ],
            )
        )

    def screen_today() -> list[ft.Control]:
        overview = state.api.overview(state.selected_id)
        name = state.selected["name"] if state.selected else "friend"
        action, due = next_action(overview)
        pending = overview["pending_count"]
        overdue = overview["overdue_count"]
        return [
            kicker("THE DAILY FIELD JOURNAL"),
            heading(f"A good day for\n{name}.", 39),
            caption("Care is a thousand little moments. Start with the next one."),
            panel(
                kicker("YOUR NEXT ACTION"),
                heading(action, 24),
                caption(due),
                primary("Add a reminder", lambda _: open_task_form(), accent=True),
                accent=True,
            ),
            ft.Row(
                controls=[
                    ft.Container(expand=True, content=panel(kicker("PENDING"), heading(str(pending), 29), caption("Care tasks"))),
                    ft.Container(expand=True, content=panel(kicker("OVERDUE"), heading(str(overdue), 29), caption("Check your dates"))),
                ]
            ),
            kicker("COMING UP"),
            *([task_row(t) for t in overview["pending_tasks"]] or [
                panel(caption("No upcoming reminders yet. Add one when you have a confirmed date."))
            ]),
            quiet("Record today's observation", lambda _: open_event_form()),
            caption("Task dates are caregiver-entered. This overview is not a clinical health assessment."),
        ]

    def screen_passport() -> list[ft.Control]:
        selected = state.selected_id
        if selected is None:
            return []
        cached = passport_cache.get(selected)
        if cached is None:
            cached = {"events": state.api.events_page(selected), "tasks": state.api.tasks_page(selected)}
            passport_cache[selected] = cached
        event_page = cached["events"]
        task_page = cached["tasks"]
        events = event_page["items"]
        tasks = task_page["items"]

        def older_events(_):
            cursor = event_page.get("next_cursor")
            if cursor:
                nxt = state.api.events_page(selected, cursor=cursor)
                event_page["items"].extend(nxt["items"])
                event_page["next_cursor"] = nxt["next_cursor"]
                render()

        def older_tasks(_):
            cursor = task_page.get("next_cursor")
            if cursor:
                nxt = state.api.tasks_page(selected, cursor=cursor)
                task_page["items"].extend(nxt["items"])
                task_page["next_cursor"] = nxt["next_cursor"]
                render()
        name = state.selected["name"] if state.selected else "Your dog"
        controls: list[ft.Control] = [
            kicker("ONE LIFE, ONE STORY"),
            heading(f"{name}'s\npassport.", 38),
            caption("Carry the important moments forward. Only a professional can verify clinical facts."),
            primary("+ Record an observation", lambda _: open_event_form(), accent=True),
            kicker("CARE HISTORY"),
        ]
        if not events:
            controls.append(panel(heading("Every story starts somewhere.", 21), caption("No care notes recorded yet.")))
        for event in events:
            controls.append(
                panel(
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[kicker(event["kind"]), caption(historical_date(event["occurred_on"]))],
                    ),
                    ft.Text(event["notes"], size=15, color=COLORS.ink),
                    caption(event_source(event)),
                )
            )
        if event_page.get("next_cursor"):
            controls.append(quiet("Load older care notes", older_events))
        controls.extend([
            rule(), kicker("ALL REMINDERS"),
            *([task_row(t) for t in tasks] or [panel(caption("No reminders recorded."))]),
            *([quiet("Load more reminders", older_tasks)] if task_page.get("next_cursor") else []),
            quiet("+ Plan care", lambda _: open_task_form()),
        ])
        return controls

    def screen_check() -> list[ft.Control]:
        ingredient_input = ft.TextField(
            label="Ingredients as printed on the label", max_length=3000,
            hint_text="For example: rice, cocoa, raisins…", multiline=True, min_lines=3,
        )
        consumed = ft.Checkbox(label="My dog may already have eaten this", value=False)
        result_section = ft.Column(spacing=12)

        def scan(_):
            if not (ingredient_input.value or "").strip():
                result_section.controls = [panel(caption("Enter the ingredients before checking."))]
                page.update()
                return
            try:
                result = state.api.food(ingredient_input.value, bool(consumed.value))
                status, lead = safe_ingredient_status(result)
                details = [
                    kicker(status), heading(lead, 24),
                    ft.Text(result.get("summary", ""), size=14, color=COLORS.ink),
                    ft.Text(result.get("next_step", "Contact a veterinarian if concerned."), size=14),
                ]
                for flag in result.get("flagged", []):
                    details.append(caption(f"Flag: {flag['ingredient']} · not vet reviewed"))
                details.append(caption("Limited educational reference, not clinical guidance. Unknown ≠ safe."))
                result_section.controls = [panel(*details)]
            except ApiError as exc:
                result_section.controls = [panel(caption(str(exc)))]
            page.update()

        return [
            kicker("THE CAREFUL CHECK"), heading("Before you\nshare a bite.", 38),
            caption("Check text from a food label against Bhow's limited educational hazard list."),
            panel(
                kicker("INGREDIENT LOOKUP"),
                ingredient_input,
                consumed,
                primary("Review ingredients", scan, accent=True),
            ),
            result_section,
            panel(kicker("BREED DISCOVERY"), heading("Not available yet.", 21),
                  caption("A validated model and representative Indian dog data are needed. No fake prediction.")),
        ]

    def screen_explore() -> list[ft.Control]:
        outdoor = state.api.outdoor_advice()
        return [
            kicker("THE DOG FIELD GUIDE"),
            heading("Curiosity is\ncare, too.", 38),
            caption("Learn, notice and support better daily routines."),
            panel(
                kicker("OUTDOOR CARE · OFFLINE REFERENCE"),
                heading(outdoor["headline"], 22),
                *[caption("• " + advice) for advice in outdoor["reminders"]],
                caption("Not based on live weather or real-time pavement temperatures."),
            ),
            panel(kicker("NOTICE"), heading("Observe the individual.", 22),
                  caption("Changes in appetite, comfort, movement or play belong in the care journal. They do not establish a diagnosis."),
                  quiet("Record an observation", lambda _: open_event_form())),
            panel(kicker("FUTURE: NEARBY HELP"), heading("Trust before pins.", 22),
                  caption("Local clinics and rescue points will appear only after a reliable provider and verification workflow are connected.")),
            panel(kicker("OUR PROMISE"), caption("No stock or AI-generated dog imagery. No fake diagnoses, services or certainty. Essential safety information remains free.")),
        ]

    def tab_selected(e) -> None:
        nonlocal tab_index
        tab_index = e.control.selected_index
        render()

    def render() -> None:
        page.controls.clear()
        if not state.dogs:
            page.navigation_bar = None
            body = [
                kicker("BHOW / WELCOME"),
                heading("Every dog deserves\na story worth keeping.", 38),
                caption("A practical, beautifully simple care journal for the dog in your life."),
                panel(
                    kicker("01 / MEET YOUR DOG"),
                    heading("Start with a name.", 23),
                    caption("No photos, breed guesses or location required."),
                    primary("Create their passport", lambda _: open_new_dog(), accent=True),
                ),
                quiet("Need help now?", emergency),
            ]
        else:
            page.navigation_bar = ft.NavigationBar(
                bgcolor=COLORS.surface,
                indicator_color=COLORS.turmeric,
                selected_index=tab_index,
                destinations=[
                    ft.NavigationBarDestination(icon=icon, label=label)
                    for icon, label in (
                        (ft.Icons.WB_SUNNY_OUTLINED, "Today"),
                        (ft.Icons.MENU_BOOK_OUTLINED, "Passport"),
                        (ft.Icons.FACT_CHECK_OUTLINED, "Check"),
                        (ft.Icons.EXPLORE_OUTLINED, "Explore"),
                    )
                ],
                on_change=tab_selected,
            )
            try:
                body = [top_bar()] + (
                    screen_today() if tab_index == 0 else
                    screen_passport() if tab_index == 1 else
                    screen_check() if tab_index == 2 else screen_explore()
                )
            except ApiError as exc:
                body = [top_bar(), panel(heading("Can't load this page.", 25), caption(str(exc)),
                    primary("Retry", lambda _: render()))]
        if message:
            body.insert(0, panel(caption(message)))
        width = min(max((page.width or 400) - 32, 300), 720)
        page.add(ft.SafeArea(content=ft.Container(
            width=width,
            content=ft.Column(spacing=20, controls=body + [ft.Container(height=24)]),
        )))
        page.update()

    render()


if __name__ == "__main__":
    ft.run(main)
