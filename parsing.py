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

    for data in loads_json("ZulipStats(2021-03-22).json"):
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

    for data in loads_json("GitStats(2021-03-22).json"):
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

    data_json = loads_json("JitsiStats(2021-03-22).json")
    for data in data_json:
        data = json.loads(line)
        #for data in loads_json("JitsiStats(2021-03-22).json"):
        for auditorium in data["auditoriums"]:
            grade["attendance_seminars"] += check_seminar(auditorium)
            try:
                if data["date"] in dates_of_poster:
                    grade["attendance_poster"] += check_project(auditorium["name"],
                                                                auditorium["classes"],
                                                                data["date"])
            except KeyError:
                pass
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


def check_poster(session):
    times_of_poster = ["13:00-14:20",
                       "14:40-16:00", "11:10-12:30", "09:30-10:50"]
    if (session["members"].count(EMAIL) > 0
            and session["classTime"] in times_of_poster):
        return True


def check_project(name, classes, date):
    count = 0
    path_date = "/home/student/student_stats/ddrustamova/dates/"+date+".txt"
    projects = [line[:-1] for line in open(path_date)]

    if name[0:7] == "project" and name[7:] in projects:
        for session in classes:
            if check_poster(session):
                count += 1

    return count
