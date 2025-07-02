from collections import Counter
from datetime import datetime

def generate_study_insights(tasks):
    insights = []

    completed_tasks = [t for t in tasks if t.completed_at]
    total = len(completed_tasks)
    print('I AM RUNNING, check if i return')
    if total >= 5:
        weekdays = [t.completed_at.strftime('%A') for t in completed_tasks]
        freq = Counter(weekdays)
        most_common_day = freq.most_common(1)[0][0]
        insights.append(f"You usually complete tasks on **{most_common_day}s**. Way to go!")
        insights.append("Amazing — you’ve completed over 5 tasks! Keep the momentum going.")


    avg_delay = [
        (t.completed_at - t.created_at).days
        for t in completed_tasks
        if t.created_at
    ]
    if avg_delay:
        avg = sum(avg_delay) / len(avg_delay)
        if avg < 1.5:
            insights.append("You're quick to complete tasks — love the focus!")
        elif avg > 4:
            insights.append("You often take a few days to finish tasks — breaking them down smaller can assist with this!")

    if total == 0:
        insights.append("No completed tasks yet — let’s get your first win on the board!")

    return insights