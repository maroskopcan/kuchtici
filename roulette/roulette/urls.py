from django.contrib import admin
from django.urls import path
from cooking.views import HomepageView, roulette, upload, del_all, ListReceiptRatingView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('roulette/', roulette, name='roulette'),
    path('upload/', upload, name='upload'),
    path('del_all/', del_all, name='del_all'),
    path('receipt_rating/', ListReceiptRatingView.as_view(), name='list_receipt_rating'),
]