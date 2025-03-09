from langchain_core.tools import tool
from asana.rest import ApiException
from core.tools.asana.config import AsanaAPIConfig

api_config = AsanaAPIConfig()
workspace_gid = api_config.workspace_gid
users_api = api_config.get_users_api()

@tool
def get_users_for_workspace():
    """Get all user's gid, name and email from a asana's workspace"""
    opts = {
        "opt_fields": "email,name", 
    }

    try:
        users = users_api.get_users_for_workspace(workspace_gid, opts)

    except ApiException as e:
        return f"It happened an error on Asana's API. Error: {e}"

    users_str = ""
    for user in users:
        users_str += f"{user}\n"

    return users_str

@tool
def get_user(user_identifier: str):
    """Get user's gid, name and email by it's gid or email."""
    opts = {
        "opt_fields": "email,name",
        "workspace": workspace_gid
    }

    try:
        user = users_api.get_user(user_identifier, opts)

    except ApiException as e:
        return f"It happened an error while searching for the following user: {user_identifier} on Asana's API. Error: {e}"

    return user