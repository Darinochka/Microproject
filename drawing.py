import dash
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from parsing import get_stat, get_stat_git_commits, get_stat_zulip_mess


def create_dates_and_counts(d):
    dates = list(d.keys())
    counts = list(d.values())
    return dates, counts


grade = get_stat()

commits_date, commits_count = create_dates_and_counts(get_stat_git_commits())
messages_date, messages_count = create_dates_and_counts(get_stat_zulip_mess())

counts = list(grade.values())

summary_counts = []
for i in range(len(counts)):
    if i == 4 or i == 5:
        summary_counts.append(counts[i]*0.5)
    else:
        summary_counts.append(int(bool(counts[i])))

summary_counts.append(round(sum(summary_counts)))

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    specs=[[{"type": "scatter"}],
           [{"type": "table"}]]
)

fig.add_trace(go.Scatter(
    x=commits_date,
    y=commits_count,
    name='commits',
    connectgaps=True
),
    row=1, col=1)

fig.add_trace(go.Scatter(
    x=messages_date,
    y=messages_count,
    name='messages',
    connectgaps=True
),
    row=1, col=1)

fig.add_trace(
    go.Table(
        header=dict(values=["Критерии", 'Количество', 'Итог']),
        cells=dict(values=[["Аккаунт в git", "Коммиты в git", "Аккаунт в Zulip",
                            "Сообщения в Zulip", "Присутствие на постерной сессии", "Присутствие на семинарах", "Всего"],
                           counts, summary_counts])
    ),
    row=2, col=1
)

fig.update_layout(
    height=900,
    plot_bgcolor='rgb(245, 245, 245)',
    showlegend=True,
    yaxis_title="Count",
    title_text="Вывод оценки активности Рустамовой Дарины",
)
fig.write_html("/home/student/student_stats/ddrustamova/ddrustamova.html")
