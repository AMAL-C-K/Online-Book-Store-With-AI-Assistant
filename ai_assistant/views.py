from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from products_app.models import Book
from .models import Conversation
from .services import ask_gemini_about_book


def book_chat_api(request, book_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    book = get_object_or_404(Book, id=book_id, is_active=True)

    question = request.POST.get("question", "").strip()

    if not question:
        return JsonResponse({"error": "Question is required"}, status=400)

    if request.user.is_authenticated:

        conversation = Conversation.objects.filter(user=request.user, book=book).first()

        if conversation is None:

            conversation = Conversation.objects.create(user=request.user, book=book)

        # Save user message
        conversation.messages.create(role="user", content=question)

        # Get all messages
        messages = conversation.messages.all()

        # Gemini
        answer = ask_gemini_about_book(book, messages)

        # Save AI message
        conversation.messages.create(role="assistant", content=answer)

        return JsonResponse({"answer": answer})

    # ==================================================
    # ANONYMOUS USER
    # ==================================================

    session_key = f"ai_chat_book_{book.id}"

    chat_history = request.session.get(session_key, [])

    # Add user question
    chat_history.append({"role": "user", "content": question})

    # Build prompt directly for anonymous user
    conversation_history = ""

    for message in chat_history:

        conversation_history += f"{message['role']}: " f"{message['content']}\n"

    prompt = f"""
You are an AI book assistant for an online bookstore.

Book title:
{book.title}

Author:
{book.author}

Genre:
{book.genre.genre}

Description:
{book.short_description}

Conversation:

{conversation_history}

Answer the user's latest question clearly and naturally.

Do not invent information about the book.
Keep the answer reasonably concise.
"""

    # Use your existing Gemini client
    from django.conf import settings
    from google import genai

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)

    answer = response.text

    # Save AI response to session
    chat_history.append({"role": "assistant", "content": answer})

    request.session[session_key] = chat_history
    request.session.modified = True

    return JsonResponse({"answer": answer})


def clear_book_chat(request, book_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    book = get_object_or_404(Book, id=book_id)

    if request.user.is_authenticated:

        Conversation.objects.filter(user=request.user, book=book).delete()

    else:

        session_key = f"ai_chat_book_{book_id}"

        request.session.pop(session_key, None)
        request.session.modified = True

    return JsonResponse({"success": True})
