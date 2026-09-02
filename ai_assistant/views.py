from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from products_app.models import Book
from .models import Conversation
from .services import ask_gemini_about_book


def book_chat_api(request, book_id):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    book = get_object_or_404(
        Book,
        id=book_id,
        is_active=True
    )

    question = request.POST.get(
        "question",
        ""
    ).strip()

    if not question:
        return JsonResponse(
            {"error": "Question is required"},
            status=400
        )

    # ==================================================
    # AUTHENTICATED USER
    # ==================================================

    if request.user.is_authenticated:

        conversation = Conversation.objects.filter(
            user=request.user,
            book=book
        ).first()

        if conversation is None:
            conversation = Conversation.objects.create(
                user=request.user,
                book=book
            )

        user_message = conversation.messages.create(
            role="user",
            content=question
        )

        messages = conversation.messages.all()

        try:

            answer = ask_gemini_about_book(
                book,
                messages
            )

        except Exception as e:

            print("\n========== GEMINI ERROR ==========")
            print("Error type:", type(e).__name__)
            print("Error:", str(e))
            print("==================================\n")

            # Remove the user message if Gemini failed
            user_message.delete()

            return JsonResponse(
                {
                    "error": (
                        "AI service is temporarily unavailable. "
                        "Please try again later."
                    )
                },
                status=503
            )

        conversation.messages.create(
            role="assistant",
            content=answer
        )

        return JsonResponse({
            "answer": answer
        })

    # ==================================================
    # ANONYMOUS USER
    # ==================================================

    session_key = f"ai_chat_book_{book.id}"

    chat_history = request.session.get(
        session_key,
        []
    )

    # Add user message
    chat_history.append({
        "role": "user",
        "content": question
    })

    try:

        answer = ask_gemini_about_book(
            book,
            chat_history
        )

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print("Error type:", type(e).__name__)
        print("Error:", str(e))
        print("==================================\n")

        # Remove failed user message
        chat_history.pop()

        return JsonResponse(
            {
                "error": (
                    "AI service is temporarily unavailable. "
                    "Please try again later."
                )
            },
            status=503
        )

    # Save AI response
    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    request.session[session_key] = chat_history
    request.session.modified = True

    return JsonResponse({
        "answer": answer
    })


def clear_book_chat(request, book_id):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    book = get_object_or_404(
        Book,
        id=book_id
    )

    if request.user.is_authenticated:

        Conversation.objects.filter(
            user=request.user,
            book=book
        ).delete()

    else:

        session_key = f"ai_chat_book_{book_id}"

        request.session.pop(
            session_key,
            None
        )

        request.session.modified = True

    return JsonResponse({
        "success": True
    })
