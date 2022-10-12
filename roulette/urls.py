from django.contrib import admin
from django.urls import path
from cooking.views import homepage_view, roulette, upload, del_all, main, \
    receipt, admin_tools, scrap, add_receipt_form, delete_rec, update_rec, \
    add_ingredients, update_rec_form, about

#from django.conf import settings
#from django.conf.urls.static import static
from cooking.views import homepage_view, roulette, upload, del_all, ListReceiptRatingView, main, receipt
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', homepage_view, name='homepage'),
    #path('', HomepageView.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('roulette/', roulette, name='roulette'),
    path('upload/', upload, name='upload'),
    path('del_all/', del_all, name='del_all'),
    path('', main), #?
#    path('roulette/', receipt), #?
    path('admin_tools/', admin_tools, name='admin_tools'),
    path('scrap/', scrap, name='scrap'),
    path('add_receipt_form/', add_receipt_form, name='add_receipt_form'),
    path('delete_rec/<int:id>', delete_rec, name='delete_rec'),
    path('update_rec/<int:id>', update_rec, name='update_rec'),
    path('add_ingredients/<int:id>', add_ingredients, name='add_ingredients'),
    path('update_rec_form/<int:id>', update_rec_form, name='update_rec_form'),

] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    path('receipt_rating/', ListReceiptRatingView.as_view(), name='list_receipt_rating'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('about/', about, name='about'),
    #path('roulette/', receipt),
]  #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)