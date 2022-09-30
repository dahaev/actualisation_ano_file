import pyodbc
from test import AllTasksInPWA, url, select, filter, test_projects
from datetime import datetime


def date(date_string):
    date_string = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    new_date = date_string.strftime("%d.%m.%Y")
    return new_date


def connecttodb():
    connection_to_db = pyodbc.connect(
        r'Driver={SQL Server};Server=DESKTOP-1EETA0V\SQLEXPRESS;Database=ano_rsi;Trustedconnection=yes;')

    cursor = connection_to_db.cursor()

    return cursor


def ReaperTasksReport():
    cursor = connecttodb()
    try:
        cursor.execute('DROP TABLE reaper_report')
    except:
        print('Отчет по реперным точкам еще не создан')

    cursor.execute(
        'CREATE TABLE reaper_report (id int IDENTITY(1,1) PRIMARY KEY, project_id VARCHAR(50) FOREIGN KEY REFERENCES projects(project_id), task_code VARCHAR(50), full_name VARCHAR(250) NOT NULL, date DATE, status VARCHAR(50) NOT NULL, RZ VARCHAR(50))')
    reaper_list = []
    reaper_tasks = AllTasksInPWA(url, select, filter)
    for i, j in enumerate(reaper_tasks):
        for let in j:
            if let['ИДПроекта'] in test_projects:
                continue
            result = (let['ИДПроекта'], let['Кодзадачи'], let['НазваниеЗадачи'], date(let['ДатаОкончанияЗадачи']),
                      let['Статусзадачи'], let['Реперныезадачи'])
            reaper_list.append(result)

    sql = 'INSERT INTO reaper_report(project_id, task_code, full_name, date, status, RZ) VALUES(?,?,?,?,?,?)'
    cursor.executemany(sql, reaper_list)
    query_report = 'SELECT projects.program, projects.project_name, reaper_report.task_code, reaper_report.full_name, reaper_report.date, reaper_report.status FROM reaper_report LEFT JOIN projects ON reaper_report.project_id = projects.project_id'
    cursor.execute(query_report)
    result = cursor.fetchall()
    return result





# a = ProjectDict()
# values = []
# for digit, value in enumerate(a):
#     s = (value['ИДПроекта'], value['ИмяПроекта'], value['Программа'], value['КодДС'], value['Полноеназваниепроекта'])
#     values.append(s)


# reaper_list = []
# reaper_tasks = AllTasksInPWA(url, select, filter)
# for i, j in enumerate(reaper_tasks):
#     for let in j:
#         if let['ИДПроекта'] in test_projects:
#             continue
#         result = (let['ИДПроекта'], let['Кодзадачи'], let['НазваниеЗадачи'], date(let['ДатаОкончанияЗадачи']), let['Статусзадачи'], let['Реперныезадачи'])
#         reaper_list.append(result)


# print(len(reaper_tasks))
# reaper_list = []
# for digit, value in enumerate(reaper_tasks):
#     ValueDigit = value[digit]
#     s = (ValueDigit['ИДПроекта'], ValueDigit['Кодзадачи'], ValueDigit['НазваниеЗадачи'], date(ValueDigit['ДатаОкончанияЗадачи']), ValueDigit['Статусзадачи'], ValueDigit['Реперныезадачи'])
#     reaper_list.append(s)
# print(f'\n{len(reaper_list)}\n')
# for i in reaper_list:
#     print(i)


# Создать таблицу Реперные точки в БД

# cursor = connecttodb()
# cursor.execute('CREATE TABLE reaper_point (id int IDENTITY(1,1) PRIMARY KEY, project_id VARCHAR(50) FOREIGN KEY REFERENCES projects(project_id), task_code VARCHAR(50), full_name VARCHAR(250) NOT NULL, date DATE, status VARCHAR(50) NOT NULL, RZ VARCHAR(50))')
# cursor.commit()
# cursor.close()

# cursor = connecttodb()
# sql = 'INSERT INTO reaper_point(project_id, task_code, full_name, date, status, RZ) VALUES(?,?,?,?,?,?)'
# cursor.executemany(sql, reaper_list)
# cursor.commit()
# cursor.close()
