import json
from requests.auth import HTTPBasicAuth
import requests

test_projects = ('2ed5b9ec-cef9-eb11-811a-00155d7f2547', '24d80de2-bca5-ec11-811f-00155d7f9c7d',
                 '38911f31-5075-ec11-b38c-c8d9d22ecdc4','0000cf75-fb12-4ffc-a404-aec4f3258a9c')

def update_url(url):
    url = url[url.find('?') + 1:]
    return url
def ResponsTasksJson():
    response = requests.get(
        'https://spanorsi.lancloud.ru/pwa/_api/ProjectData/Проекты?$select=КодДС,ИДПроекта,ИмяПроекта,'
        'Руководительпроектов,Программа,Подпрограмма,Полноеназваниепроекта&$format=json',
        auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
    data = response.json()['value']
    return data


def ProjectDict():
    project = []
    data = ResponsTasksJson()
    for projects in data:
        if projects['ИДПроекта'] in test_projects:
            continue
        project.append(projects)
    return project


project_id = 'a40b2ab3-c30f-ec11-8833-0c5415e5f39e'
url = "https://spanorsi.lancloud.ru/pwa/_api/ProjectData/Задачи?$format=json"
select = '&$select=ИмяПроекта,НазваниеЗадачи,Кодзадачи,ИДПроекта'
inlinecount = '&$inlinecount=allpages'
filter = "&$filter=ИДПроекта eq guid'"
url = url + select
url_all = url + select

def ProjectTasks(url, select='', filter=''):
    inline_url = url + select + filter + '&$inlinecount=allpages'
    ReapersList = []
    response = requests.get(inline_url, auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
    data_count = response.json()['odata.count']
    print(f'Всего задач в проекте: {data_count}')
    NextLinkUrl = ''
    count_tasks = 0
    while True:
        response = requests.get(url + select + NextLinkUrl + filter, auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
        data = response.json()['value']
        count_tasks += len(data)
        ReapersList.append(data)
        try:
            if response.json()['odata.nextLink']:
                NextLinkUrl = '&' + update_url(response.json()['odata.nextLink'])
                select, filter = '', ''
                continue
        except:
            break
    print('Загружено задач: ', count_tasks)
    return ReapersList


def AllTasksInPWA(url):
    TasksList = []
    inline_url = url + '&$inlinecount=allpages'
    print(inline_url)
    response = requests.get(inline_url, auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
    data_count = response.json()['odata.count']
    print(f'Всего задач для выгрузки: {data_count}')
    NextLinkUrl = ''
    count_tasks = 0
    while True:
        response = requests.get(url + NextLinkUrl, auth=HTTPBasicAuth('conteq_1@ano-rsi.ru', 'BesB8288'))
        data = response.json()['value']
        count_tasks += len(data)
        TasksList.append(data)
        print(f'Загружено задач: {count_tasks}')
        try:
            if response.json()['odata.nextLink']:
                NextLinkUrl = '&' + response.json()['odata.nextLink']
                continue
        except:
            break
    print('Загружено задач: ', count_tasks)
    return TasksList

# a = AllTasksInPWA(url_all)
#
# with open('AllProjectTasks.txt', 'w', encoding='utf-8') as f:
#     json.dump(a, f, ensure_ascii=False, indent=4)

# a = ProjectTasks(url, project_id, filter)
# with open('project_tasks.txt', 'w', encoding='utf-8') as f:
#     json.dump(a, f, ensure_ascii=False, indent=4)
