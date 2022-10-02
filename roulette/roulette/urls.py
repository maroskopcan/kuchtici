from django.contrib import admin
from django.urls import path
from cooking.views import HomepageView, roulette, upload, del_all, ListReceiptRatingView
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('roulette/', roulette, name='roulette'),
    path('upload/', upload, name='upload'),
    path('del_all/', del_all, name='del_all'),
    path('receipt_rating/', ListReceiptRatingView.as_view(), name='list_receipt_rating'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]