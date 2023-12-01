from os import getenv

import stripe
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, reverse, redirect

from .models import Item, Order

stripe.api_key = getenv('STRIPE_SECRET_KEY')


def session_data_func(item: Item, data: dict) -> dict:
    """
       Adds an item to the session data dictionary.
       Args:
           item (Item): The item to be added.
           data (dict): The session data dictionary.
       Returns:
           dict: The updated session data dictionary.
       """
    data['line_items'].append({
        'price_data': {
            'unit_amount': item.price * 100,
            'currency': item.currency,
            'product_data': {
                'name': item.name
            },
        },
        'quantity': 1,
    })
    return data


def buy_item(request, pk: int) -> JsonResponse:
    """
   Retrieves an item with the specified primary key and generates a checkout session for purchasing the item.
   Parameters:
       request (HttpRequest): The HTTP request object.
       pk (int): The primary key of the item to be purchased.
   Returns:
       JsonResponse: A JSON response containing the session ID and the Stripe public key for the checkout session.
       If the request method is 'GET':
           - If the item with the specified primary key exists, a checkout session is created using the item data.
           - If the item does not exist, a JSON response with an error message is returned.
       If the request method is not 'GET', a JSON response with an error message indicating that the method is not
       allowed is returned.
       """
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item does not exist'})
        session_data = {
            'mode': 'payment',
            'success_url': request.build_absolute_uri(reverse('Payment:success')),
            'cancel_url': request.build_absolute_uri(reverse('Payment:cancel')),
            'line_items': []
        }
        session_data_func(item, session_data)
        session = stripe.checkout.Session.create(**session_data)
        return JsonResponse({'session_id': str(session.id), 'key': getenv('STRIPE_PUBLIC_KEY')})
    else:
        return JsonResponse({'error': 'Method not allowed'})


def item_view(request, pk: int):
    item = Item.objects.get(pk=pk)
    return render(request, 'Payment/item.html', {'item': item})


def buy_order(request, pk):
    """
    Retrieve an order by its primary key and initiate the payment process.
    Parameters:
        - request: The HTTP request object.
        - pk: The primary key of the order to be retrieved.
    Returns:
        - If the order with the given primary key does not exist, an HTTP response with the message "Order does not exist" is returned.
        - If the order is empty (does not have any items), an HTTP response with the message "Order cannot be empty. Add Item" is returned.
        - Otherwise, the payment process is initiated and a redirect to the payment session URL is returned.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return HttpResponse("Order does not exist")
    items = order.items.all()
    if not items:
        return HttpResponse("Order cannot be empty. Add Item")
    session_data = {
        'mode': 'payment',
        'success_url': request.build_absolute_uri(reverse('Payment:success')),
        'cancel_url': request.build_absolute_uri(reverse('Payment:cancel')),
        'line_items': [
        ]}
    n = 0
    for item in items:
        session_data_func(item, session_data)
        if order.tax and order.tax.active:
            session_data['line_items'][n].update({'tax_rates': [order.tax.tax_hash]})
            n += 1
        if order.discount:
            session_data.update({'discounts': [{'coupon': f'{order.discount.discount_hash}'}]})
    print('meow')
    session = stripe.checkout.Session.create(**session_data)
    print('meow')
    return redirect(session.url, code=301)


def success_view(request):
    return JsonResponse({'success': True})


def cancel_view(request):
    return JsonResponse({'success': False})


def index(request):
    return render(request, 'Payment/index.html')
