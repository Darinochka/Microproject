import json

EMAIL = "ddrustamova@miem.hse.ru"
grade = {
    "account_git": 0,
    "commits_git": 0,
    "account_zulip": 0,
    "messages_zulip": 0,
    "attendance_poster": 0,
    "attendance_seminars": 0}


def loads_json(file_name):
    with open("/home/student/rawData/"+file_name, "r") as f:
        return json.loads(f.read())


def get_stat_zulip_mess():
    "return dict of date and count of messages"
    messages = {}

    for data in loads_json("ZulipStats.json"):
        if data["email"] == EMAIL:
            grade["account_zulip"] = 1
            grade["messages_zulip"] += len(data["messages"])
            for message in data["messages"]:
                if message["timestamp"][:10] in messages:
                    messages[message["timestamp"][:10]] += 1
                else:
                    messages[message["timestamp"][:10]] = 1

    return messages


def get_stat_git_commits():
    "return dict date and count of commits"
    commits = {}

    for data in loads_json("GitStats.json"):
        if data["email"] == EMAIL:
            grade["account_git"] = 1

            for project in data["projects"]:
                try:
                    grade["commits_git"] += len(project["commits"])
                    for commit in project["commits"]:
                        if commit["committed_date"][:10] in commits:
                            commits[commit["committed_date"][:10]] += 1
                        else:
                            commits[commit["committed_date"][:10]] = 1
                except KeyError:
                    pass

    return commits


def get_stat():
    dates_of_poster = ["2021-01-25", "2021-01-26",
                       "2021-01-27", "2021-01-28", "2021-01-29"]

    data_json = loads_json("JitsiClasses.json")
    for data in data_json:
        for auditorium in data["auditoriums"]:
            grade["attendance_seminars"] += check_seminar(auditorium)

    data_json = loads_json("JitsiSession.json")
    for data in data_json:
        if (data["username"] == EMAIL
                and data["date"] in dates_of_poster):
            grade["attendance_poster"] += check_project(data["room"],
                                                        data["date"])
    return grade


def check_seminar(auditorium):
    count = 0
    times_of_seminars = ["18:10-19:30", "16:20-17:40", "19:40-21:00"]

    for seminar in auditorium["classes"]:
        try:
            if (seminar["discipline"] == "Проектный семинар (1 курс) (рус)"
                and seminar["classTime"] in times_of_seminars
                    and seminar["members"].count(EMAIL) > 0):
                count += 1
        except KeyError:
            pass
    return count


def check_project(room, date):
    path_date = "/home/student/student_stats/ddrustamova/dates/"+date+".txt"
    projects = [line[:-1] for line in open(path_date)]

    if room[0:7] == "project" and room[7:] in projects:
        return 1
    return 0
