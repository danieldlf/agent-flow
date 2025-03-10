from asana import (
    Configuration, 
    ApiClient, 
    TasksApi, 
    UsersApi, 
    TeamsApi, 
    UserTaskListsApi,
    ProjectsApi
    )
from config import Config

class AsanaAPIConfig:
    def __init__(self):
        self._api_client = self.get_client()
        self._workspace_gid = self.get_workspace_gid()

    def get_client(self):
        configuration = Configuration()
        configuration.access_token = Config.ASANA_API_TOKEN
        api_client = ApiClient(configuration)

        return api_client
    
    def get_workspace_gid(self):
        return Config.ASANA_WORKSPACE_GID

    def get_tasks_api(self):
        return TasksApi(self.api_client)
    
    def get_users_api(self):
        return UsersApi(self.api_client)
    
    def get_teams_api(self):
        return TeamsApi(self.api_client)
    
    def get_user_task_lists_api(self):
        return UserTaskListsApi(self.api_client)
    
    def get_projects_api(self):
        return ProjectsApi(self.api_client)

    @property
    def api_client(self):
        return self._api_client
    
    @property
    def workspace_gid(self):
        return self._workspace_gid