from typing import Literal
from datetime import date

from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from asana.rest import ApiException

from core.tools.asana.config import AsanaAPIConfig
from core.services import LLMService
from core.prompts import choose_project_prompt

api_config = AsanaAPIConfig()
workspace_gid = api_config.workspace_gid
tasks_api = api_config.get_tasks_api()
user_task_list_api = api_config.get_user_task_lists_api()
projects_api = api_config.get_projects_api()
llm = LLMService().get_model("ollama", model="llama3.1")
today = date.today()

@tool
def list_user_tasks():
    """List all user's tasks"""
    gid = get_user_task_list_gid()
    opts = {
    'limit': 50,
    'opt_fields': 
        "name,\
        completed,\
        completeda_at,\
        created_at,\
        due_on,\
        due_at,\
        assignee,\
        assignee.name,\
        assignee_status,\
        projects,\
        projects.name,\
        memberships.section,\
        memberships.section.name,\
        notes,\
        permalink_url",
    }

    tasks = tasks_api.get_tasks_for_user_task_list(gid, opts)

    tasks_str = ""
    for task in tasks:
        tasks_str += f"{task}\n"

    return tasks_str

@tool
def list_project_tasks(project_name: str, status: Literal["all", "completed", "pending"] = "all", assignee: str = None, overdue_only: bool = False):
    """
    List all tasks in a project with optional filters.
    
    Args:
        project_name (str): The name of the project.
        status (str): Filter tasks by status. Options: "all", "completed", "pending".
        assignee (str): Filter tasks assigned to a specific person (optional).
        overdue_only (bool): If True, returns only overdue tasks.
    
    Returns:
        str: Formatted task list.
    """
    try:
        project_gid = get_project_gid(project_name)
        opts = {
            "limit": 50,
            "opt_fields": 
            "name,\
            completed,\
            completeda_at,\
            created_at,\
            due_on,\
            due_at,\
            assignee,\
            assignee.name,\
            assignee_status,\
            projects,\
            projects.name,\
            memberships.section,\
            memberships.section.name,\
            notes,\
            permalink_url",
        }
        
        tasks = tasks_api.get_tasks_for_project(project_gid, opts)

        if status == "completed":
            tasks = [t for t in tasks if t.get('completed')]
        elif status == "pending":
            tasks = [t for t in tasks if not t.get('completed')]

        if assignee:
            tasks = [t for t in tasks if t.get('assignee', {}).get('name') == assignee]

        if not tasks:
            return "No tasks found for the given filters."
        
        if overdue_only:
            tasks = [
                task for task in tasks 
                if not task.get('completed') and task.get('due_on') and date.fromisoformat(task['due_on']) < today
            ]

        tasks_str = ""
        for task in tasks:
            task_name = task['name']
            due_date = task.get('due_on', 'No Due Date')
            assignee_name = task.get('assignee', {}).get('name', 'Unassigned')
            is_overdue = False
            days_overdue = None

            if due_date != 'No Due Date':
                due_date_obj = date.fromisoformat(due_date)
                if due_date_obj < today and not task.get('completed'):
                    is_overdue = True
                    days_overdue = (today - due_date_obj).days
                else:
                    days_remaining = (due_date_obj - today).days

            if is_overdue:
                tasks_str += f"- {task_name} (Atrasada por {days_overdue} dias, Data de Conclusão: {due_date}, Responsável: {assignee_name})\n"
            else:
                tasks_str += f"- {task_name} (Não atrasada faltando {days_remaining} dias para data de conclusão, Data de Conclusão: {due_date}, Responsável: {assignee_name})\n"

        return tasks_str

    except ApiException as e:
        return "Error retrieving tasks."

@tool
def search_task(text: str):
    """Search a task by it's title and description."""
    opts = {
    'text': text,
    'opt_fields': 
        "name,\
        assignee,\
        assignee.name,\
        completed,\
        completed_at,\
        completed_by,\
        completed_by.name,\
        created_at,\
        created_by"
    }

    tasks = tasks_api.search_tasks_for_workspace(workspace_gid, opts)

    tasks_str = ""
    for task in tasks:
        tasks_str += f"{task}\n"

    return tasks_str

def get_user_task_list_gid(user_gid="me"):
    opts = {
    'opt_fields': 
        "name,\
        owner,\
        workspace"
    }

    user_task_list = user_task_list_api.get_user_task_list_for_user(user_gid, workspace_gid, opts)

    return user_task_list["gid"]

def get_project_gid(project_name: str):
    opts = {
    'limit': 50,
    'archived': False,
    'opt_fields': "name"
    }

    projects = list(projects_api.get_projects_for_workspace(workspace_gid, opts))

    projects_str = ""
    for project in projects:
        projects_str += f"{project["name"]}\n"

    chain = choose_project_prompt | llm | StrOutputParser()
    project_exact_name = chain.invoke({"projects": projects_str, "input": project_name})

    project_gid = 0
    for project in projects:
        if project["name"].strip().lower() == project_exact_name.strip().lower():
            project_gid = project["gid"]

    return project_gid