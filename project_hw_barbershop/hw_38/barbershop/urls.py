
from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/master-services/', views.get_master_services, name='master_services'),
    path('review/create/', views.create_review, name='create_review'),
    path('orders/create/', views.create_order, name='create_order'),
    path('review/thanks/', views.thanks_for_review, name='review_thanks')
]
