
from django.contrib import admin
from django.urls import path , include , re_path
from rest_framework import permissions

# drste moshkel az IntelliSense vscode
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)




urlpatterns = [
    path('admin/', admin.site.urls),



    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    path('api/acnt/',include('core.urls')),
    path('api/news/',include('news.urls')),
    path('api/events/',include('events.urls')),
    path('api/articles/',include('articles.urls')),
    path('api/comments/',include('comments.urls')),
    path('api/dashboard/',include('dashboard.urls')),

]

# 1 ta user admin bszm postman ---- 1 user member ---- 1 user normal
# ba hame GET konam OK -------- ba hame Post,Put,Delete konam normal ha Error
# event bsazam , update deleta konam , register konam
# havaset bsh ke ma permissions ro az news bordam to core ke all app avilble