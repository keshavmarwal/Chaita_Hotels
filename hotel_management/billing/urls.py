from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BillViewSet, GenerateBillView, BillDetailView

router = DefaultRouter()
router.register('bills', BillViewSet)

urlpatterns = router.urls + [
    path('bills/generate/<int:booking_id>/', GenerateBillView.as_view()),  # POST
    path('bills/detail/<int:booking_id>/', BillDetailView.as_view()),      # GET
]