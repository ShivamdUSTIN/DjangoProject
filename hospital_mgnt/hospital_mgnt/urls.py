
# from django.contrib import admin
# from django.urls import path, include
# from two_factor.urls import urlpatterns as tf_urls

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('hospital.urls')),
#     path('account/', include(tf_urls)),  # Without namespace
# ]

from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(tf_urls)),
    path('', include('hospital.urls')),
]

