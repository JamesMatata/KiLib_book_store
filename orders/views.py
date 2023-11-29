from django.http import JsonResponse
from django.shortcuts import render

from basket.basket import Basket
from orders.models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', deliveryPoint='deliveryPoint',
                                         deliveryPoint2='deliveryPoint2', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'],
                                         quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response
