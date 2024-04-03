from django.contrib import admin
from django.urls import path, include
from news.yasg import urlpatterns as doc_url




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('news.api.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]



urlpatterns+=doc_url