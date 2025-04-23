from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from detection import views as detection_views  # Import views from detection app for direct path usage

# ---------------------------------------------------
# URL Patterns
# This list maps URL paths to views in the Django app.
# ---------------------------------------------------
urlpatterns = [
    # Admin panel URL (e.g., http://localhost:8000/admin/)
    path('admin/', admin.site.urls),

    # Include all URLs from the detection app's urls.py
    path('', include('detection.urls')),

    # Home page or root URL directly mapped to image upload view
    # This might be redundant if detection.urls already includes this view at the root
    path('', detection_views.upload_image, name='upload_image'),

    # User registration page (e.g., http://localhost:8000/register/)
    path('register/', detection_views.register_user, name='register'),

    # User login page (e.g., http://localhost:8000/login/)
    path('login/', detection_views.login_user, name='login'),

    # User logout endpoint (e.g., http://localhost:8000/logout/)
    path('logout/', detection_views.logout_user, name='logout'),

    # Serve media files during development (e.g., uploaded images)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ---------------------------------------------------
# Notes:
# - In production, serving media files should be handled by the web server (e.g., Nginx).
# - The path('', ...) usage twice may cause a conflict — 
#   it's recommended to let one source handle the root URL.
# ---------------------------------------------------
