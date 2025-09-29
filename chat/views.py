from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


# Página web
def chat_page(request):
    return render(request, "chat/chat.html")


# Inicializar modelo y cadena
llm = OllamaLLM(model="llama3")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un amigo confiable y empático que conversa con el usuario sobre su día."),
    ("human", "{input}")
])

chain = prompt | llm

# Diccionario para almacenar historial por sesión
chat_histories = {}

def get_history(session_id: str):
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

# Crear la cadena con historial usando RunnableWithMessageHistory
chat_chain = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")
            session_id = data.get("session_id", "anon")
            response = chat_chain.invoke(
                {"input": user_message},
                config={"configurable": {"session_id": session_id}}
)


            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            response = chat_chain.invoke(
                {"input": user_message},
                config={"configurable": {"session_id": session_id}}
            )

            # Asumiendo que response es un string
            return JsonResponse({"reply": response})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
