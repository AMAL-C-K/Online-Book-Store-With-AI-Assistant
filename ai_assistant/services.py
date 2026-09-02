import time

from django.conf import settings
from google import genai
from google.genai.errors import ServerError


# Create Gemini client once
client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def ask_gemini_about_book(book, messages):

    conversation_history = ""

    for message in messages:

        # Django ConversationMessage object
        if hasattr(message, "role"):
            role = message.role
            content = message.content

        # Anonymous session dictionary
        else:
            role = message.get("role", "")
            content = message.get("content", "")

        conversation_history += (
            f"{role}: {content}\n"
        )

    prompt = f"""
You are an AI book assistant for an online bookstore.

Book information:

Title:
{book.title}

Author:
{book.author}

Genre:
{book.genre.genre}

Description:
{book.short_description}

Conversation history:

{conversation_history}

Instructions:

1. Answer the user's latest question clearly and naturally.
2. Use the book information provided above.
3. Remember the conversation history.
4. Do not invent information about the book.
5. If the information is not available, say so.
6. Keep the answer reasonably concise.
"""

    # Retry temporary Gemini 503 errors
    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except ServerError as e:

            # Gemini 503 / temporary server problem
            if getattr(e, "status_code", None) == 503:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                # All retries failed
                raise Exception(
                    "Gemini is temporarily unavailable. "
                    "Please try again later."
                )

            # Other Gemini server errors
            raise

    # Safety fallback
    raise Exception(
        "Gemini is temporarily unavailable. "
        "Please try again later."
    )
