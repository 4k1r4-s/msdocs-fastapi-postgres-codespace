from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("環境変数 GOOGLE_API_KEY が設定されていません。")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=API_KEY)

def create_knowledge_base(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    texts = CharacterTextSplitter(separator="\n", chunk_size=100, chunk_overlap=20).split_text(raw_text)
    docs = [Document(page_content=t) for t in texts]
    return FAISS.from_documents(docs, HuggingFaceEmbeddings(model_name="all-mpnet-base-v2"))

knowledge_base = create_knowledge_base("Caustic.txt")
system_message = SystemMessage(content="あなたはコースティックです。")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.message
    retriever = knowledge_base.as_retriever()
    context_text = "\n\n".join([doc.page_content for doc in retriever.invoke(user_input)])
    prompt = f"以下は参考情報です。\n{context_text}\n\n質問: {user_input}"

    conversation_history = [system_message, HumanMessage(content=prompt)]
    response = llm.invoke(conversation_history)
    return {"reply": response.content}