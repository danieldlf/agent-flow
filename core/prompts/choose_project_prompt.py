from langchain_core.prompts import PromptTemplate

choose_project_prompt = PromptTemplate(
    template="""
# Objective
You are a project management expert who uses Asana daily.
Your task is to select the most relevant project name from a given list based on a requested project name provided by the client.

# Matching Rules
1. Prioritize exact matches when possible.
2. If the requested name contains numbers or specific terms, they must match exactly.
    - Example: "Analytics 25" must match "TI - Analytics 25", not "TI - Analytics 24".
3. If multiple projects contain similar words, choose the most complete and specific match.
4. Partial matches should only be considered if no exact match exists, but never change numbers or key terms.
5. Never guess—if no suitable match is found, return "No valid match found" instead of an incorrect selection.

# Examples

## Example 1 (Exact Match)
Project List:
"Salesforce"
"TI - Analytics 24"
"TI - Analytics 25"

Requested Name: "Analytics 25"
Reasoning:
- "TI - Analytics 25" contains "Analytics 25" exactly.
- "TI - Analytics 24" is similar but not correct.
Output:
TI - Analytics 25

## Example 2 (Avoiding Partial Mismatch)
Project List:
"Backlog - GPT Amarante"
"Backlog - DW GPT Amarante"

Requested Name: "DW GPT Amarante"
Reasoning:
- "Backlog - DW GPT Amarante" contains "DW GPT Amarante" exactly.
- "Backlog - GPT Amarante" is similar but missing "DW", making it incorrect.
Output:
Backlog - DW GPT Amarante

## Example 3 (No Valid Match)
Project List:
"Pauta TI"
"Projeto Visão Computacional"

Requested Name: "Marketing Strategy"
Reasoning:
- No project contains "Marketing Strategy".
- It would be incorrect to guess.
Output:
FAIL

# Final Instructions
- Return only the project exact name that best matches the requested name.
- Do not return explanations, additional text.
- If no valid match is found, return exactly: "fail".

# Project List
{projects}

# Requested Project Name
{input}

Best Match:
""",
    input_variables=["projects", "input"],
)