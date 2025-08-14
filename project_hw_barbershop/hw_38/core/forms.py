from django import forms
from .models import Review, Master, Order, Service


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    master = forms.ModelChoiceField(
        queryset=Master.objects.filter(is_active=True),
        label='Мастер',
        empty_label='Выберите мастера',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        label='Оценка',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    client_name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )

    text = forms.CharField(
        label='Текст отзыва',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Поделитесь вашим впечатлением...'
        })
    )

    class Meta:
        model = Review
        fields = ['master', 'client_name', 'rating', 'text']


class OrderForm(forms.ModelForm):
    master = forms.ModelChoiceField(
        queryset=Master.objects.filter(is_active=True),
        label='Мастер',
        empty_label='Выберите мастера',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    client_name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )

    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67',
            'type': 'tel'
        })
    )

    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш email'
        })
    )

    appointment_date = forms.DateTimeField(
        label='Дата и время записи',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )

    notes = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ваши пожелания...'
        })
    )

    class Meta:
        model = Order
        fields = ['master', 'client_name', 'phone', 'email', 'appointment_date', 'services', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'master' in kwargs['initial']:
            master = kwargs['initial']['master']
            self.fields['services'].queryset = master.services.all()
        elif self.is_bound and 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                master = Master.objects.get(id=master_id)
                self.fields['services'].queryset = master.services.all()
            except (ValueError, TypeError, Master.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['services'].queryset = self.instance.master.services.all()
        else:
            self.fields['services'].queryset = Service.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')

        if master and services:
            for service in services:
                if service not in master.services.all():
                    raise forms.ValidationError(
                        f"Мастер {master.name} не предоставляет услугу '{service.name}'. "
                        "Пожалуйста, выберите только услуги, доступные у этого мастера."
                    )

        return cleaned_data
