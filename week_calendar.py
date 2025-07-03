def generate_week_data(today, tasks, exams):
    from datetime import timedelta

    start = today - timedelta(days=today.weekday())
    week_days = []

    for i in range(7):
        current_day = start + timedelta(days=i)
        day_tasks = [t for t in tasks if t.due_date and t.due_date.date() == current_day.date()]
        day_exams = [e for e in exams if e.date and e.date.date() == current_day.date()]

        week_days.append({
            'date': current_day,
            'is_today': current_day.date() == today.date(),
            'tasks': day_tasks,
            'exams': day_exams
        })

    return week_days