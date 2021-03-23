import dash
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from parsing import get_stat, get_stat_git_commits, get_stat_zulip_mess,get_stat_jitsi_poster, get_stat_jitsi_classes, grade


def create_dates_and_counts(d):
    dates = list(d.keys())
    counts = list(d.values())
    return dates, counts


commits_date, commits_count = create_dates_and_counts(get_stat_git_commits())
messages_date, messages_count = create_dates_and_counts(get_stat_zulip_mess())
seminars_date, seminars_count = create_dates_and_counts(get_stat_jitsi_classes())
poster_date, poster_count = create_dates_and_counts(get_stat_jitsi_poster())

counts = list(grade.values())

summary_counts = []
for i in range(len(counts)):
    if i == 4 or i == 5:
        summary_counts.append(counts[i]*0.5)
    else:
        summary_counts.append(int(bool(counts[i])))

summary = round(sum(summary_counts))
summary_counts.append(summary - summary%10)

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
    name='Коммиты',
    connectgaps=True
),
    row=1, col=1)

fig.add_trace(go.Scatter(
    x=messages_date,
    y=messages_count,
    name='Сообщения',
    connectgaps=True
),
    row=1, col=1)

fig.add_trace(go.Scatter(
    x=seminars_date,
    y=seminars_count,
    name='Присутствие на семиинарах',
    connectgaps=True
),
    row=1, col=1)

fig.add_trace(go.Scatter(
    x=poster_date,
    y=poster_count,
    name='Присутствие на постерной сессиии',
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
    yaxis_title="Количество",
    title_text="Вывод оценки активности Рустамовой Дарины",
)
fig.write_html("/home/student/student_stats/ddrustamova/ddrustamova.html")
