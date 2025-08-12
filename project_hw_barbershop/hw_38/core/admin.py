from django.contrib import admin
from .models import Service, Master, Order, Review


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'status')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating')
