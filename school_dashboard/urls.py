
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import  views as auth_views
from django.conf import settings
from django.conf.urls.static import static 
from api.views import StudentViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the API URLs
    path('', include('core.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
