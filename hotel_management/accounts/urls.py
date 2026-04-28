from django.urls import path
from .views import LoginView ,TestAdminView, TestReceptionistView ,UserUpdateView, UserDeactivateView ,TestHRView ,TestManagerView, UserListCreateView 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('admin-test/', TestAdminView.as_view()),
    path('rec-test/', TestReceptionistView.as_view()),
    path('hr-test/' ,TestHRView.as_view()),
    path('man-test/',TestManagerView.as_view()),
    path('users/', UserListCreateView.as_view()),
    path('users/<int:pk>/', UserUpdateView.as_view()),
    path('users/<int:pk>/deactivate/', UserDeactivateView.as_view()),
]