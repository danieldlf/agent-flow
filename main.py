from core.services import LLMService

model = LLMService.get_model("ollama", model="llama3.1")
response = model.run("Quem é o atual presidente dos Estados unidos?")

print(response)