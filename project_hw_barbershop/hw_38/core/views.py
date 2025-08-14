from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET

from .forms import ReviewForm, OrderForm
from .models import Master, Review, Order


def landing(request):
    masters = Master.objects.all()
    reviews = Review.objects.all().select_related('master')[:6]
    return render(request, 'landing.html', {'masters': masters, 'reviews': reviews})


def thanks(request):
    return render(request, 'thanks.html')


@login_required(login_url='/admin/login')
def orders_list(request):
    orders = Order.objects.all().select_related('master').prefetch_related('services').order_by('-date_created')

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


@login_required(login_url='/admin/login')
def order_detail(request, order_id):
    order = Order.objects.select_related('master').prefetch_related('services').filter(id=order_id).annotate(
        total_price=Sum('services__price'),
    ).first()
    if not order:
        raise Http404(
            "No Order matches the given query."
        )
    return render(request, 'order_detail.html', {'order': order})


@require_GET
def get_master_services(request):
    master_id = request.GET.get('master_id')
    try:
        master = Master.objects.get(id=master_id, is_active=True)
        services = [{
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': str(service.price),
            'duration': service.duration
        } for service in master.services.all()]
        return JsonResponse({'services': services})
    except Master.DoesNotExist:
        return JsonResponse({'error': 'Мастер не найден'}, status=404)


def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_thanks')
    else:
        form = ReviewForm()

    return render(request, 'review_form.html', {'form': form})


@login_required(login_url='/admin/login')
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = OrderForm()

    return render(request, 'order_form.html', {'form': form})


def thanks_for_review(request):
    return render(request, 'thanks_for_review.html')
