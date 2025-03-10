from flask import Blueprint, jsonify, request
from langchain_core.globals import set_debug
from core.agent import app

set_debug(True)

agent_bp = Blueprint("agent", __name__)

@agent_bp.route("/invoke", methods=["POST"])
def invoke():
    query = request.args.get("query")

    final_state = app.invoke(
        {
            "messages": 
            [
                {"role": "system", "content": f"You are a helpful assistant. Respond only in portuguese."},
                {"role": "user", "content": query}
            ]
        },
        config={"configurable": {"thread_id": 42}}
    )

    return jsonify({"response": final_state["messages"][-1].content}), 200