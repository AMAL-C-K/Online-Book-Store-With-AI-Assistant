from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart_app.models import Cart
from .models import Order


# ==============================
# CHECKOUT
# ==============================

@login_required(login_url='signin')
def checkout(request):

    # GET CART ITEMS

    cart_items = Cart.objects.filter(
        user=request.user,
        ordered=False
    )

    # EMPTY CART CHECK

    if not cart_items.exists():
        return redirect('cart')

    # TOTAL AMOUNT

    total = sum(item.total() for item in cart_items)

    # PLACE ORDER

    if request.method == 'POST':

        for item in cart_items:

            # CREATE ORDER

            Order.objects.create(

                user=request.user,

                book=item.book,

                quantity=item.quantity,

                total_amount=item.total(),

                payment_method='Cash On Delivery',

                status='Order Placed'
            )

            # STOCK UPDATE

            book = item.book

            if book.stock >= item.quantity:

                book.stock -= item.quantity

                book.save()

            # REMOVE CART ITEM

            item.delete()

        return redirect('orders')

    return render(request, 'checkout.html', {

        'cart_items': cart_items,

        'total': total
    })


# ==============================
# ORDERS PAGE
# ==============================

@login_required(login_url='signin')
def orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(request, 'orders.html', {

        'orders': orders
    })