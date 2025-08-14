from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Master, Review, Order


def landing(request):
    masters = Master.objects.all()
    reviews = Review.objects.all()[:6]
    return render(request, 'landing.html', {'masters': masters, 'reviews': reviews})


def thanks(request):
    return render(request, 'thanks.html')


@login_required(login_url='/admin/login')
def orders_list(request):
    orders = Order.objects.all().order_by('-date_created')

    search_query = str(request.GET.get('search', ''))
    search_by_client = request.GET.get('search_by_client', 'on') == 'on'
    search_by_phone = request.GET.get('search_by_phone', '') == 'on'
    search_by_comment = request.GET.get('search_by_comment', '') == 'on'

    if search_query and (search_by_client or search_by_phone or search_by_comment):
        query = Q()

        if search_by_client:
            query |= Q(client_name__icontains=search_query)

        if search_by_phone:
            query |= Q(phone__icontains=search_query)

        if search_by_comment:
            query |= Q(comment__icontains=search_query)

        orders = orders.filter(query)

    context = {
        'orders': orders,
        'search_query': search_query,
        'search_by_client': search_by_client,
        'search_by_phone': search_by_phone,
        'search_by_comment': search_by_comment,
    }
    return render(request, 'order_list.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_detail.html', {'order': order})
