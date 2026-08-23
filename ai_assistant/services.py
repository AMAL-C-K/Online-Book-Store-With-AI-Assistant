from django.conf import settings
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def ask_gemini_about_book(book, messages):

    conversation_history = ""

    for message in messages:

        conversation_history += f"{message.role}: {message.content}\n"

    prompt = f"""
                You are an AI book assistant for an online bookstore.

                You are helping the user discuss the following book.

                BOOK INFORMATION

                Title: {book.title}

                Author: {book.author}

                Genre: {book.genre.genre}

                Description: {book.short_description}

                CONVERSATION HISTORY {conversation_history}


                Instructions: 

                1. Answer the user's latest question clearly.
                2. Keep the conversation natural.
                3. Use the book information provided above.
                4. Remember the previous messages in the conversation.
                5. Do not invent facts about the book.
                6. If the information is not available, say so.
                7. Keep answers reasonably concise.
            """

    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt,)

    return response.text
