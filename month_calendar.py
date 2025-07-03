def generate_month_data(year, month, tasks, exams):
    from calendar import monthrange
    from datetime import date, timedelta

    num_days = monthrange(year, month)[1]
    first_day = date(year, month, 1)
    today = date.today()
    calendar_days = []

    for day_num in range(num_days):
        current_day = first_day + timedelta(days=day_num)

        day_tasks = [t for t in tasks if t.due_date and t.due_date.date() == current_day]
        day_exams = [e for e in exams if e.date and e.date.date() == current_day]

        calendar_days.append({
            'date': current_day,
            'is_today': current_day == today,
            'tasks': day_tasks,
            'exams': day_exams
        })

    return calendar_days
