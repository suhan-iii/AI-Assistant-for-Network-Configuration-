from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from config_app.views import ConfigViewSet

router = DefaultRouter()
router.register(r'configs', ConfigViewSet, basename='config')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
