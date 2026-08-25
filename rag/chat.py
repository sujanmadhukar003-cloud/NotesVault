from .retrieve import retrieve_chunks
from .generate import generate_answer


conversation_history = []


def build_context(chunks):

    context = ""

    for i, chunk in enumerate(chunks):

        context += f"""
========================
SOURCE {i+1}
========================

Semester : {chunk['semester']}
Subject  : {chunk['subject']}
Unit     : {chunk['unit']}
Topic    : {chunk['topic']}
"""

        if chunk.get("section_title"):

            context += f"""
Section : {chunk['section_title']}
"""

        if chunk.get("definition"):

            context += f"""

Definition:
{chunk['definition']}
"""

        if chunk.get("content"):

            context += f"""

Content:
{chunk['content']}
"""

        if chunk.get("example"):

            context += f"""

Example:
{chunk['example']}
"""

        if chunk.get("section_content"):

            context += f"""

Section Content:
{chunk['section_content']}
"""

        context += "\n------------------------\n"

    return context


def build_history():

    history = ""

    for msg in conversation_history[-6:]:

        history += f"""
{msg['role']}: {msg['content']}
"""

    return history


def chat(question):

    search_query = question

    previous_user_messages = [

        msg["content"]

        for msg in conversation_history

        if msg["role"] == "User"
    ]


    if previous_user_messages:

        search_query = (
            " ".join(previous_user_messages[-3:])
            + " "
            + question
        )

    chunks = retrieve_chunks(search_query)

    context = build_context(chunks)

    history = build_history()

    full_question = f"""
Conversation History:
{history}

Current Question:
{question}
"""

    answer = generate_answer(
        context,
        full_question
    )

    conversation_history.append({
        "role": "User",
        "content": question
    })

    conversation_history.append({
        "role": "Assistant",
        "content": answer
    })

    return answer