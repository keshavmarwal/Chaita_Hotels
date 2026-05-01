from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, CreateOrderView, OrderListView, GenerateBillView

router = DefaultRouter()
router.register('menu', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
    path('order/create/', CreateOrderView.as_view()),
    path('order/list/', OrderListView.as_view()),
    path('bill/<int:order_id>/', GenerateBillView.as_view()),
]