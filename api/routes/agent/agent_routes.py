from flask import Blueprint, jsonify, request

from core.services import LLMService

llm = LLMService.get_model("ollama", model="llama3.1")

agent_bp = Blueprint("agent", __name__)

@agent_bp.route("/invoke", methods=["POST"])
def invoke():
    query = request.args.get("query")
    response = llm.run(query)

    return jsonify({"response": response}), 200