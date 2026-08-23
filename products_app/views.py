from django.shortcuts import render
from .models import Book, Genre
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ai_assistant.services import ask_gemini_about_book
from ai_assistant.models import Conversation
from django.contrib.auth.decorators import login_required




# Display all books with sorting and pagination

def all_books(request):

     

    books = Book.objects.all()
    genres = Genre.objects.all()

    sort = request.GET.get('sort')

    if sort == 'a-z':
        book = books.order_by('title')
    
    elif sort == 'low-high':
        book = books.order_by('price')

    elif sort == 'high-low':
        book = books.order_by('-price')
    
    else:
        book = books.order_by('-created_at')

    paginator = Paginator(book, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'genres':genres,
        'page_obj':page_obj
    }
    return render(request, 'products.html', context)


def genre_wise_books(request, slug):

    books = Book.objects.filter(genre__slug=slug)
    genre = Genre.objects.get(slug=slug)

    sort = request.GET.get('sort')

    if sort == 'a-z':
        books = books.order_by('title')

    elif sort == 'low-high':
        books = books.order_by('price')

    elif sort == 'high-low':
        books = books.order_by('-price')

    else:
        books = books.order_by('-created_at')

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'genre': genre
    }

    return render(request, 'genre_wise_products.html', context)


def single_book(request, genre_slug, book_slug):
    
    book = get_object_or_404(Book, slug = book_slug, genre__slug = genre_slug)

    messages = []


    # ========================================
    # LOGGED-IN USER
    # ========================================

    if request.user.is_authenticated:

        conversation = Conversation.objects.filter(
            user=request.user,
            book=book
        ).first()


        if conversation:

            messages = conversation.messages.order_by(
                "-created_at"
            )


    # ========================================
    # ANONYMOUS USER
    # ========================================

    else:

        session_key = f"ai_chat_book_{book.id}"


        chat_history = request.session.get(
            session_key,
            []
        )


        # Convert session data to objects
        # so the existing template can use
        # message.role and message.content

        class SessionMessage:

            def __init__(
                self,
                role,
                content
            ):

                self.role = role

                self.content = content


        messages = [

            SessionMessage(
                message["role"],
                message["content"]
            )

            for message in reversed(chat_history)

        ]


    return render(
        request,
        "single_product.html",
        {
            "book": book,
            "messages": messages,
        }
    )

def search_book(request):

    query = request.GET.get('q', '').strip()
    books = Book.objects.none()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__genre__icontains=query)
        ).distinct()

    sort = request.GET.get('sort')

    if sort == 'a-z':
        books = books.order_by('title')

    elif sort == 'low-high':
        books = books.order_by('price')

    elif sort == 'high-low':
        books = books.order_by('-price')

    else:
        books = books.order_by('-created_at')

    paginator = Paginator(books, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj
    }

    return render(request, 'search_book.html', context)