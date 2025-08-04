
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/acnt/',include('core.urls')),
    path('api/news/',include('news.urls')),
    path('api/events/',include('events.urls')),
    path('api/articles/',include('articles.urls')),

]

# 1 ta user admin bszm postman ---- 1 user member ---- 1 user normal
# ba hame GET konam OK -------- ba hame Post,Put,Delete konam normal ha Error
# event bsazam , update deleta konam , register konam
# havaset bsh ke ma permissions ro az news bordam to core ke all app avilble