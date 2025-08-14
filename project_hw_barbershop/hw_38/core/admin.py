from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Service, Master, Order, Review


class AppointmentDateFilter(admin.SimpleListFilter):
    """Кастомный фильтр для даты записи"""
    title = _('Дата записи')
    parameter_name = 'appointment_date'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Сегодня')),
            ('tomorrow', _('Завтра')),
            ('this_week', _('На этой неделе')),
        )

    def queryset(self, request, queryset):
        from datetime import datetime, timedelta
        today = datetime.today().date()

        if self.value() == 'today':
            return queryset.filter(appointment_date__date=today)
        if self.value() == 'tomorrow':
            tomorrow = today + timedelta(days=1)
            return queryset.filter(appointment_date__date=tomorrow)
        if self.value() == 'this_week':
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            return queryset.filter(appointment_date__date__range=[start_week, end_week])


class ServiceInline(admin.TabularInline):
    """Инлайн для услуг в заказе"""
    model = Order.services.through
    extra = 1
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги"


class ReviewInline(admin.TabularInline):
    """Инлайн для отзывов о мастере"""
    model = Review
    extra = 1
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"
    fields = ('client_name', 'rating', 'text', 'created_at')
    readonly_fields = ('created_at',)


def mark_as_confirmed(modeladmin, request, queryset):
    """Действие: пометить заказы как подтвержденные"""
    queryset.update(status='confirmed')


mark_as_confirmed.short_description = 'Подтвердить выбранные заказы'


def mark_as_cancelled(modeladmin, request, queryset):
    """Действие: пометить заказы как отмененные"""
    queryset.update(status='cancelled')


mark_as_cancelled.short_description = 'Отменить выбранные заказы'


def mark_as_in_progress(modeladmin, request, queryset):
    """Действие: пометить заказы как "В работе"""
    queryset.update(status='in_progress')


mark_as_in_progress.short_description = 'Отметить как "В работе"'


def mark_as_completed(modeladmin, request, queryset):
    """Действие: пометить заказы как завершенные"""
    queryset.update(status='completed')


mark_as_completed.short_description = 'Отметить как завершенные'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'phone', 'master', 'status', 'appointment_date', 'total_price')
    list_filter = ('status', 'master', AppointmentDateFilter)
    search_fields = ('client_name', 'phone')
    list_editable = ('status',)
    actions = [mark_as_confirmed, mark_as_cancelled, mark_as_in_progress, mark_as_completed]
    inlines = [ServiceInline]

    def total_price(self, obj):
        return sum(service.price for service in obj.services.all())
    total_price.short_description = 'Общая стоимость заказа'


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active')
    list_filter = ('is_active', 'services')
    search_fields = ('name',)
    inlines = [ReviewInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating')
