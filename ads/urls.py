from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list_view, name='ad-list'),
    path('ads/<int:pk>/', views.ad_detail_view, name='ad-detail'),
    path('ads/create/', views.ad_create_view, name='ad-create'),
    path('ads/<int:pk>/edit/', views.ad_edit_view, name='ad-edit'),
    path('ads/<int:pk>/delete/', views.ad_delete_view, name='ad-delete'),
    path('ads/<int:ad_id>/propose/', views.proposal_create_view, name='proposal-create'),
    path('proposals/', views.proposal_list_view, name='proposal-list'),
    path('proposals/<int:pk>/', views.proposal_detail_view, name='proposal-detail'),
    path('proposals/<int:pk>/<str:new_status>/', views.proposal_update_status_view, name='proposal-update-status'),
]
