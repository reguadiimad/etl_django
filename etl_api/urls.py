from django.urls import path
from .views.admin_view import AdminListCreateView, AdminDeleteView, AdminLoginView, ForgotPasswordView, AdminUpdateView,change_password, NewsLetterEmailsListCreateAPIView
from rest_framework_simplejwt import views as jwt_views
from .views.inscrption_view import InscriptionListView, InscriptionDetailView, InscriptionCreateView, InscriptionUpdateView
from .views.news_view import NewsCreateView, NewsTranslatedListView, NewsUpdateView, NewsDeleteView
from .views.condidats_view import condidats_view
from .views.contact_views import ContactFormView, ContactFormListView

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
    path('inscriptions/<int:id>/update/', InscriptionUpdateView.as_view(), name='inscription-update'),

    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news-translated/', NewsTranslatedListView.as_view(), name='news-translated'),
    path('news/latest-translated/', NewsTranslatedListView.as_view(), name='latest-news-translated'),
    path('news/<int:pk>/update/', NewsUpdateView.as_view(), name='news-update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),

    path('newsletter-emails/', NewsLetterEmailsListCreateAPIView.as_view(), name='newsletter-emails'),



    path('condidats/', condidats_view, name='condidats'),

    path('contact/submit/', ContactFormView.as_view(), name='contact-form'),
    path('contact/list/', ContactFormListView.as_view(), name='contact-form-list'),




    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
