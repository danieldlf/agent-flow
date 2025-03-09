from flask import Flask
from api.routes.agent import agent_bp

app = Flask(__name__)
app.register_blueprint(agent_bp)