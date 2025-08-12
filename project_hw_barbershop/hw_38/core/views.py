from django.shortcuts import render
from .data_source import *


def landing(request):
    return render(request, 'landing.html', {'masters': masters, 'services': services})


def thanks(request):
    return render(request, 'thanks.html')


def orders_list(request):
    if request.user.is_staff:
        return render(request, 'order_list.html', {'orders': orders})
    return render(request, 'order_list.html')


def order_detail(request, order_id):
    for order in orders:
        if order['id'] != order_id:
            continue
        for master in masters:
            if master['id'] != order['master_id']:
                continue
            return render(
                request,
                'order_detail.html',
                {'order': order, 'order_id': order_id, 'master': master},
            )

    return render(request, 'order_detail.html', {'order_id': order_id})
