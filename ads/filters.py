import django_filters
from .models import Ad, ExchangeProposal

class AdFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Поиск')

    class Meta:
        model = Ad
        fields = ['category', 'condition']

    def filter_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value) | queryset.filter(description__icontains=value)

class ProposalFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='ad_sender__user__username', lookup_expr='icontains', label='Отправитель')
    receiver = django_filters.CharFilter(field_name='ad_receiver__user__username', lookup_expr='icontains', label='Получатель')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = ExchangeProposal
        fields = ['sender', 'receiver', 'status']
