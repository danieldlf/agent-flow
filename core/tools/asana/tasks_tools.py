from langchain_core.tools import tool
from core.tools.asana.config import AsanaAPIConfig

class TasksTools:
    def __init__(self):
        api_config = AsanaAPIConfig()
        self.workspace_gid = api_config.workspace_gid
        self.tasks_api = api_config.get_tasks_api()

"""     @tool
    def list_tasks():
        ... """