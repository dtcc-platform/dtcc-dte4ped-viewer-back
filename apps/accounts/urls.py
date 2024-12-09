from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts import api_views

api_router_react = DefaultRouter()
api_router_react.register(r'accounts', api_views.AccountsViewSet, basename='api-accounts')

urlpatterns = [
    path(r'react/', include(api_router_react.urls))
]

