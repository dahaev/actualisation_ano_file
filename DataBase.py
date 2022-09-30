class Task:

    def __init__(self, project_id, code_task, name, task_fill):
        self.project_id = project_id
        self.code_task = code_task
        self.name = name


    def __repr__(self):
        return f'{self.name}'


task = Task



