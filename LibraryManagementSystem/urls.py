from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from LibraryManagementSystem import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name="homepage"),
    path('<slug:category_slug>', views.Home, name="category_wise_post"),
    path('books/', include('books.urls')),
    path('user/', include('user.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)