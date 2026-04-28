from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuestViewSet, GuestDetailView

router = DefaultRouter()
router.register('', GuestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/details/', GuestDetailView.as_view()),
]