import dash
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from parsing import getStat, getStatGitCommits, getStatZulipMess


def createDatesAndCounts(d):
    dates = list(d.keys())
    counts = list(d.values())
    return [dates, counts]


grade = getStat()

commits = createDatesAndCounts(getStatGitCommits())
messages = createDatesAndCounts(getStatZulipMess())
count = list(grade.values())

bool_count = []
for i in range(len(count)):
    if i == 4 or i == 5:
        bool_count.append(count[i]*0.5)
    else:
        bool_count.append(int(bool(count[i])))

bool_count.append(round(sum(bool_count)))

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    specs=[[{"type": "scatter"}],
           [{"type": "table"}]]
)

fig.add_trace(go.Scatter(
    x=commits[0],  # date
    y=commits[1],  # count
    name='commits',
    connectgaps=True
),
    row=1, col=1)

fig.add_trace(go.Scatter(
    x=messages[0],  # date
    y=messages[1],  # value
    name='messages',
    connectgaps=True
),
    row=1, col=1)

fig.add_trace(
    go.Table(
        header=dict(values=["Критерии", 'Количество', 'Итог']),
        cells=dict(values=[["Аккаунт в git", "Коммиты в git", "Аккаунт в Zulip",
                            "Сообщения в Zulip", "Присутствие на постерной сессии", "Присутствие на семинарах", "Всего"],
                           count, bool_count])
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
