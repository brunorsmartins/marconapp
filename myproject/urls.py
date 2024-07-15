from django.contrib import admin
from django.urls import path, include
from finance import views as finance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('finance.urls')),
    path('', finance_views.home, name='home'),
]
