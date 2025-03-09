""" from api import app

if __name__ == "__main__":
    app.run(debug=True, port=5000) """

from core.agent.agent import app
from langchain_core.globals import set_debug

set_debug(True)

final_state = app.invoke(
    {"messages": [{"role": "user", "content": ""}]},
    config={"configurable": {"thread_id": 42}}
)

print(final_state["messages"][-1].content)