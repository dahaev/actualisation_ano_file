import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://spanorsi.lancloud.ru/pwa/_api/ProjectData/Задачи?$format=json"

test_projects = ('2ed5b9ec-cef9-eb11-811a-00155d7f2547', '24d80de2-bca5-ec11-811f-00155d7f9c7d')

"""Запрос на получение всех проектов и их названий"""


def ResponsTasksJson():
    response = requests.get(
        'https://spanorsi.lancloud.ru/pwa/_api/ProjectData/Проекты?$select=КодДС,ИДПроекта,ИмяПроекта,'
        'Руководительпроектов,Программа,Подпрограмма,Полноеназваниепроекта&$format=json',
        auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
    data = response.json()['value']
    return data


"""Получаем ИД и название всех проектов кроме Кремля и Шаблона КСГ и храним в project
Список из словарей с ИД и названием"""


def ProjectDict():
    project = []
    data = ResponsTasksJson()
    for projects in data:
        if projects['ИДПроекта'] in test_projects:
            continue
        project.append(projects)

    with open('project_list.txt', 'w') as pr_list:
        json.dump(project, pr_list, ensure_ascii=False, indent=4)
    return project


"""Забираем все задачи из проекта"""


def AllProjectTasks():
    url = "https://spanorsi.lancloud.ru/pwa/_api/ProjectData/Задачи?$format=json&" \
          "$select=ИДПроекта,ИмяПроекта,НазваниеЗадачи,Кодзадачи&"
    ReapersList = []
    response = requests.get(
        url + "$inlinecount=allpages",
        auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
    print(url + "$select=ИДПроекта,ИмяПроекта,НазваниеЗадачи,Кодзадачи&$inlinecount=allpages")
    data_count = int(response.json()['odata.count'])
    print(data_count)
    data = response.json()['value']
    ReapersList.append(data)
    print('Первая итерация пройдена')
    count = 0
    print("Вход в цикл")
    while True:
        count += 1
        print('Итерация: ', count)
        NextDataLink = response.json()['odata.nextLink']
        print()
        print(url + '$' + str(NextDataLink))
        response = requests.get(
            url + str(NextDataLink),
            auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
        data = response.json()['value']
        ReapersList.append(data)
        if response.json()['deltaLink']:
                break
    return ReapersList


