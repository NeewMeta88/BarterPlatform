from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from ads.views import AdViewSet, ExchangeProposalViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
from ads import views as ads_views

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ads')
router.register(r'proposals', ExchangeProposalViewSet, basename='proposals')

schema_view = get_schema_view(
    openapi.Info(
        title="Barter API",
        default_version='v1',
        description="Документация API для платформы обмена вещами",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include('ads.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='ads/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='ad-list'), name='logout'),
    path('register/', ads_views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Подключаем маршруты API
    # маршруты для документации API добавляются ниже
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
