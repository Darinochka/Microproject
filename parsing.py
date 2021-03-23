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
            for message in data["messages"]:
                if message["timestamp"] in messages:
                    messages[message["timestamp"]] += 1
                else:
                    messages[message["timestamp"]] = 1

    grade["messages_zulip"] = sum(messages.values())

    return messages


def get_stat_git_commits():
    "return dict date and count of commits"
    commits = {}

    for data in loads_json("GitStats.json"):
        if data["email"] == EMAIL:
            grade["account_git"] = 1

            for project in data["projects"]:
                try:
                    for commit in project["commits"]:
                        if commit["committed_date"] in commits:
                            commits[commit["committed_date"]] += 1
                        else:
                            commits[commit["committed_date"]] = 1
                except KeyError:
                    pass
    grade["commits_git"] = sum(commits.values())
    
    return commits


def get_stat():
    return grade

def get_stat_jitsi_poster():
    dates_of_poster = ["2021-01-25", "2021-01-26",
                       "2021-01-27", "2021-01-28", "2021-01-29"]
    posters = {}

    data_json = loads_json("JitsiSession.json")
    for data in data_json:
        if (data["username"] == EMAIL
                and data["date"] in dates_of_poster):
            if data["date"] in posters:
                posters[data["date"]] += check_project(data["room"],
                                                        data["date"])
            else:
                posters[data["date"]] = 0
    grade["attendance_poster"] = sum(posters.values())

    return posters
    
def get_stat_jitsi_classes():
    count = 0
    times_of_seminars = ["18:10-19:30", "16:20-17:40", "19:40-21:00"]
    seminars = {}

    data_json = loads_json("JitsiClasses.json")
    for data in data_json:
        for auditorium in data["auditoriums"]:
            for seminar in auditorium["classes"]:
                try:
                    if (seminar["discipline"] == "Проектный семинар (1 курс) (рус)"
                        and seminar["classTime"] in times_of_seminars
                            and seminar["members"].count(EMAIL) > 0):
                        if data["date"] in seminars:
                            seminars[data["date"]] += 1
                        else:
                            seminars[data["date"]] = 1
                except KeyError:
                    pass
    grade["attendance_seminars"] = sum(seminars.values())   
    return seminars;

def check_project(room, date):
    path_date = "/home/student/student_stats/ddrustamova/dates/"+date+".txt"
    projects = [line[:-1] for line in open(path_date)]

    if room[0:7] == "project" and room[7:] in projects:
        return 1
    return 0
