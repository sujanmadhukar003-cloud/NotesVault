from database import get_db_connection
import faiss
import pickle

from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT
    n.id,
    n.semester,
    n.subject,
    n.unit,
    n.topic,
    n.definition,
    n.content,
    n.example,
    ts.section_title,
    ts.section_content

FROM notes n

LEFT JOIN topic_sections ts
ON n.id = ts.topic_id
""")

rows = cursor.fetchall()

documents = []
metadata = []

for row in rows:

    (
        note_id,
        semester,
        subject,
        unit,
        topic,
        definition,
        content,
        example,
        section_title,
        section_content
    ) = row

    # -----------------------------
    # MAIN TOPIC DOCUMENT
    # -----------------------------

    main_doc = f"""
Semester: {semester}
Subject: {subject}
Unit: {unit}
Topic: {topic}

Definition:
{definition if definition else ""}

Content:
{content if content else ""}

Example:
{example if example else ""}
"""

    documents.append(main_doc)

    metadata.append({
        "semester": semester,
        "subject": subject,
        "unit": unit,
        "topic": topic,

        "definition": definition,
        "content": content,
        "example": example,

        "section_title": None,
        "section_content": None
    })

    # -----------------------------
    # SECTION DOCUMENT
    # -----------------------------

    if section_title and section_content:

        section_doc = f"""
Semester: {semester}
Subject: {subject}
Unit: {unit}
Topic: {topic}

Section:
{section_title}

Content:
{section_content}
"""

        documents.append(section_doc)

        metadata.append({
            "semester": semester,
            "subject": subject,
            "unit": unit,
            "topic": topic,

            "definition": None,
            "content": None,
            "example": None,

            "section_title": section_title,
            "section_content": section_content
        })

print(f"Documents created: {len(documents)}")

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    "vector_db/faiss.index"
)

with open(
    "vector_db/metadata.pkl",
    "wb"
) as f:
    pickle.dump(metadata, f)

print("FAISS index created successfully.")