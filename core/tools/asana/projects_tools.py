from langchain_core.tools import tool
from core.tools.asana.config import AsanaAPIConfig

api_config = AsanaAPIConfig()
workspace_gid = api_config.workspace_gid
projects_api = api_config.get_projects_api()

@tool
def get_all_projects():
    """List all projects (GID and name) available for the user."""
    opts = {
    'limit': 50,
    'archived': False,
    'opt_fields': "name"
    }

    projects = projects_api.get_projects_for_workspace(workspace_gid, opts)

    projects_str = ""
    for project in projects:
        projects_str += f"{project}\n"

    return projects_str