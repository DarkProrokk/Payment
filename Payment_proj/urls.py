from django.contrib import admin
from django.urls import path, include
from Payment.views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include(('Payment.urls', 'Payment'), namespace='Payment')),
    path('', index)
]
