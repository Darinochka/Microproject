import json

EMAIL = "ddrustamova@miem.hse.ru"
PATH = "/home/student/rawData/"
grade = {
    "account_git": 0,
    "commits_git": 0,
    "account_zulip": 0,
    "messages_zulip": 0,
    "attendance_poster": 0,
    "attendance_seminars": 0}


def getStatZulipMess():
    "return dict of date and count of messages"
    messages = {}
    count_messages_zulip = 0
    with open(PATH+"ZulipStats(2021-03-22).json", "r") as f:
        data_json = json.loads(f.read())
        for data in data_json:
            if data["email"] == EMAIL:
                grade["account_zulip"] = 1
                grade["messages_zulip"] += len(data["messages"])
                for message in data["messages"]:
                    if message["timestamp"][:10] in messages:
                        messages[message["timestamp"][:10]] += 1
                    else:
                        messages[message["timestamp"][:10]] = 1

    return messages


def getStatGitCommits():
    "return dict date and count of commits"
    commits = {}
    with open(PATH+"GitStats(2021-03-22).json", "r") as f:
        data_json = json.loads(f.read())
        for data in data_json:

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
                    except:
                        pass
    return commits


def getStat():
    dates_of_poster = ["2021-01-25", "2021-01-26",
                       "2021-01-27", "2021-01-28", "2021-01-29"]

    with open(PATH+"JitsiStats(2021-03-22).json", "r") as f:
        for line in f:
            data = json.loads(line)

            for auditorium in data["auditoriums"]:

                grade["attendance_seminars"] += CheckSeminar(auditorium)

                try:
                    if data["date"] in dates_of_poster:
                        grade["attendance_poster"] += CheckProject(auditorium["name"],
                                                                   auditorium["classes"],
                                                                   data["date"])
                except:
                    pass
    return grade


def CheckSeminar(auditorium):
    count = 0
    times_of_seminars = ["18:10-19:30", "16:20-17:40", "19:40-21:00"]

    for seminar in auditorium["classes"]:
        try:
            if (seminar["discipline"] == "Проектный семинар (1 курс) (рус)"
                and seminar["classTime"] in times_of_seminars
                    and seminar["members"].count(EMAIL) > 0):
                count += 1
        except:
            pass
    return count


def CheckPoster(session):
    times_of_poster = ["13:00-14:20",
                       "14:40-16:00", "11:10-12:30", "09:30-10:50"]
    if (session["members"].count(EMAIL) > 0
        and session["classTime"] in times_of_poster):
        return True


def CheckProject(name, classes, date):
    count = 0
    path_date = PATH+"/dates/"+date+".txt"
    projects = [line[:-1] for line in open(path_date)]

    if name[0:7] == "project" and name[7:] in projects:
        for session in classes:
            if CheckPoster(session):
                count += 1

    return count
