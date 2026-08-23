# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from products_app.models import Book

from .models import Cart


# ==================================
# CART PAGE
# ==================================

@login_required(login_url='signin')
def cart(request):

    cart_items = Cart.objects.filter(
        user=request.user,
        ordered=False
    ).order_by('-created_at')

    total = sum(item.total() for item in cart_items)

    context = {

        'cart_items': cart_items,

        'total': total
    }

    return render(request, 'cart.html', context)


# ==================================
# ADD TO CART
# ==================================

@login_required(login_url='signin')
def add_to_cart(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    cart_item, created = Cart.objects.get_or_create(

        user=request.user,

        book=book,

        ordered=False
    )

    # IF PRODUCT ALREADY EXISTS

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    return redirect('cart')


# ==================================
# QUANTITY PLUS
# ==================================

@login_required(login_url='signin')
def quantity_plus(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart_item.quantity += 1

    cart_item.save()

    return redirect('cart')


# ==================================
# QUANTITY MINUS
# ==================================

@login_required(login_url='signin')
def quantity_minus(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    # IF QUANTITY GREATER THAN 1

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect('cart')


# ==================================
# REMOVE ITEM
# ==================================

@login_required(login_url='signin')
def remove(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')