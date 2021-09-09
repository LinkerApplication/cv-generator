from django.contrib import admin
from django.urls import path, include

from .auto_docs_urls import urlpatterns as swagger

urlpatterns = [
    path('admin/', admin.site.urls),
]


# other urls
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]


# our urls
urlpatterns += [

]


# swagger urls
urlpatterns += swagger
