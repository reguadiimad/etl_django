from django.urls import path
from .views.admin_view import AdminListCreateView, AdminDeleteView, AdminLoginView, ForgotPasswordView, AdminUpdateView,change_password
from rest_framework_simplejwt import views as jwt_views
from .views.inscrption_view import InscriptionListView, InscriptionDetailView, InscriptionCreateView

urlpatterns = [
    path('admins/', AdminListCreateView.as_view(), name='admin-list-create'),
    path('admins/<int:pk>/', AdminDeleteView.as_view(), name='admin-delete'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path('update/<str:admin_id>/', AdminUpdateView.as_view(), name='admin-update'),
    path('change-password/<str:admin_id>/', change_password, name='change-password'),  # Change to <str:admin_id>

    path('inscriptions/', InscriptionListView.as_view(), name='inscription-list'),
    path('inscriptions/<int:pk>/', InscriptionDetailView.as_view(), name='inscription-detail'),
    path('inscriptions/create/', InscriptionCreateView.as_view(), name='inscription-create'),


    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
