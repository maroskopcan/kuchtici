from django.contrib import admin
from django.urls import path
from cooking.views import homepage_view, roulette, upload, del_all, main, receipt
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('admin/', admin.site.urls),
    path('roulette/', roulette, name='roulette'),
    path('upload/', upload, name='upload'),
    path('del_all/', del_all, name='del_all'),
    path('', main),
    path('roulette/', receipt),

] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)