"""
Generate iCalendar file from GRID task list
Creates importable .ics file for calendar applications
"""

from datetime import datetime, timedelta

from icalendar import Calendar, Event


def generate_task_calendar():
    """Generate iCalendar file from task list"""
    cal = Calendar()
    cal.add("prodid", "-//GRID TaskCalendar//grid.ai//")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("x-wr-calname", "GRID Implementation Tasks")
    cal.add("x-wr-timezone", "UTC")

    # Start tomorrow
    start_date = datetime.now().date() + timedelta(days=1)

    tasks = [
        {
            "summary": "Homework: Railways & Steam Engine Era Research",
            "description": "Complete industrial revolution timeline, document inventors, analyze impact",
            "duration": 3,  # days
        },
        {
            "summary": "NER Service System Component Upgrade",
            "description": "Design system component interface, implement entity extraction pipeline",
            "duration": 7,
        },
        {
            "summary": "Communication Discovery - Week 2: Semantic Routing",
            "description": "Build SemanticRouter with NER integration, add risk-based routing",
            "duration": 5,
        },
        {
            "summary": "Communication Discovery - Week 3: Context Bridges",
            "description": "Implement ContextBridge, create metaphor mapping (railway → software)",
            "duration": 5,
        },
        {
            "summary": "Communication Discovery - Week 4: Discovery Engine",
            "description": "Build DiscoveryEngine pattern detection, analyze communication logs",
            "duration": 5,
        },
        {
            "summary": "Communication Discovery - Week 5: Feedback Loop",
            "description": "Implement FeedbackSynthesizer, create learning loop",
            "duration": 5,
        },
        {
            "summary": "Test Suite Alignment - Week 1: Foundation",
            "description": "Create test_commons/, extract fixtures, build shared infrastructure",
            "duration": 5,
        },
    ]

    current_date = start_date
    for task in tasks:
        event = Event()
        event.add("summary", task["summary"])
        event.add("description", task["description"])

        # All-day events
        event.add("dtstart", current_date)
        event.add("dtend", current_date + timedelta(days=task["duration"]))
        event.add("dtstamp", datetime.now())
        event.add("status", "CONFIRMED")
        event.add("transp", "OPAQUE")

        # Add categories/tags
        if "Homework" in task["summary"]:
            event.add("categories", "Education")
        elif "Communication Discovery" in task["summary"]:
            event.add("categories", "Development,High-Priority")
        elif "NER" in task["summary"]:
            event.add("categories", "Development,Backend")
        elif "Test" in task["summary"]:
            event.add("categories", "QA,Infrastructure")

        cal.add_component(event)

        # Move to next task start date
        current_date += timedelta(days=task["duration"])

    # Save calendar file
    filepath = "e:/grid/task_calendar_import.ics"
    with open(filepath, "wb") as f:
        f.write(cal.to_ical())

    print(f"✅ Calendar file generated: {filepath}")
    print(f"📅 Total tasks: {len(tasks)}")
    print(f"📆 Timeline: {start_date} to {current_date}")

    return filepath


if __name__ == "__main__":
    generate_task_calendar()
