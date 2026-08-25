from database import get_db_connection


CHUNK_SIZE = 500


def chunk_text(text, chunk_size=CHUNK_SIZE):

    if not text:
        return []

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def process_notes():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT semester,
               subject,
               unit,
               topic,
               content,
               definition,
               example
        FROM notes
    """)

    rows = cursor.fetchall()

    conn.close()

    all_chunks = []

    for row in rows:

        semester, subject, unit, topic, content, definition, example = row

        combined_text = f"""
        Topic: {topic}

        Definition:
        {definition if definition else ""}

        Content:
        {content if content else ""}

        Example:
        {example if example else ""}
        """

        chunks = chunk_text(combined_text)

        for chunk in chunks:

            all_chunks.append({
                "semester": semester,
                "subject": subject,
                "unit": unit,
                "topic": topic,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    chunks = process_notes()

    print(f"Total chunks: {len(chunks)}")

    print("\nSample Chunk:\n")

    print(chunks[0])