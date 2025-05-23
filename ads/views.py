from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdForm, ExchangeProposalForm
from .filters import AdFilter, ProposalFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Ad):
            return obj.user == request.user
        elif isinstance(obj, ExchangeProposal):
            return True
        return False

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'condition']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().order_by('-created_at')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ad_sender', 'ad_receiver', 'status']

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user))
        return qs

    def perform_create(self, serializer):
        proposal = serializer.save(status='pending')
        if proposal.ad_sender.user != self.request.user:
            proposal.delete()
            raise PermissionDenied("Вы можете предлагать обмен только от имени своего объявления.")

    def perform_update(self, serializer):
        proposal = self.get_object()
        if self.request.user != proposal.ad_receiver.user:
            raise PermissionDenied("Только владелец объявления-получателя может принять или отклонить предложение.")
        serializer.save()

# HTML views
def ad_list_view(request):
    ads = Ad.objects.all().order_by('-created_at')
    f = AdFilter(request.GET, queryset=ads)
    return render(request, 'ads/ad_list.html', {
        'ads': f.qs,
        'filter': f
    })

def ad_detail_view(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'ads/register.html', {'form': form})

@login_required
def ad_create_view(request):
    form = AdForm(request.POST or None)
    if form.is_valid():
        ad = form.save(commit=False)
        ad.user = request.user
        ad.save()
        return redirect('ad-detail', pk=ad.pk)
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def ad_edit_view(request, pk):
    try:
        ad = Ad.objects.get(pk=pk)
    except Ad.DoesNotExist:
        messages.error(request, "Объявление не найдено.")
        return redirect('ad-list')

    if ad.user != request.user:
        messages.error(request, "Вы не можете редактировать чужое объявление.")
        return redirect('ad-list')

    form = AdForm(request.POST or None, instance=ad)
    if form.is_valid():
        form.save()
        messages.success(request, "Объявление успешно обновлено.")
        return redirect('ad-detail', pk=ad.pk)

    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def ad_delete_view(request, pk):
    try:
        ad = Ad.objects.get(pk=pk)
    except Ad.DoesNotExist:
        messages.error(request, "Объявление не найдено.")
        return redirect('ad-list')

    if ad.user != request.user:
        messages.error(request, "Вы не можете удалить чужое объявление.")
        return redirect('ad-list')

    if request.method == 'POST':
        ad.delete()
        messages.success(request, "Объявление удалено.")
        return redirect('ad-list')

    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

@login_required
def proposal_create_view(request, ad_id):
    target_ad = get_object_or_404(Ad, pk=ad_id)
    form = ExchangeProposalForm(request.POST or None, user=request.user)
    if form.is_valid():
        proposal = form.save(commit=False)
        proposal.ad_receiver = target_ad
        proposal.status = 'pending'
        proposal.save()
        return redirect('ad-detail', pk=ad_id)
    return render(request, 'ads/proposal_form.html', {'form': form, 'target_ad': target_ad})

@login_required
def proposal_list_view(request):
    proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user) | ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    proposal_filter = ProposalFilter(request.GET, queryset=proposals)
    return render(request, 'ads/proposal_list.html', {
        'proposals': proposal_filter.qs,
        'filter': proposal_filter
    })

@login_required
def proposal_update_status_view(request, pk, new_status):
    proposal = get_object_or_404(ExchangeProposal, pk=pk, ad_receiver__user=request.user)
    if new_status in ['accepted', 'rejected']:
        proposal.status = new_status
        proposal.save()
    return redirect('proposal-list')

@login_required
def proposal_detail_view(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    if request.method == 'POST' and request.user == proposal.ad_receiver.user:
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'rejected']:
            proposal.status = new_status
            proposal.save()
            return redirect('proposal-detail', pk=pk)
    return render(request, 'ads/proposal_detail.html', {'proposal': proposal})