# System prompt for the chat system.
CHAT_SYSTEM_ = """You are an assistant with chat and question-answering capabilities.
Answer all questions to the best of your ability.
If you don't know the answer, just say that you don't know. 
You have access to a database. 
<Database-Description>
{db_context}.
</Database-Description>

{retrieval_context}
"""

CHAT_SYSTEM = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.

Question: {input} 

Context: {retrieval_context}

Answer:
"""