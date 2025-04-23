# ------------------------------------------------------------
# Django URL Configuration for the Skin Disease Detector App
# ------------------------------------------------------------

from django.urls import path
from . import views  # Import views from the current app
from django.contrib.auth import views as auth_views  # Import built-in auth views

# Define all URL patterns that map to view functions
urlpatterns = [

    # Home/Root URL - Upload image for prediction
    path('', views.upload_image, name='upload_image'),
    # → This is the default landing page ("/")
    # → It displays a form for users to upload skin images for disease prediction

    # Profile Page - View user profile & recent predictions
    path('profile/', views.profile_view, name='profile'),
    # → Displays profile details and list of previous predictions
    # → Accessible only to logged-in users

    # Edit Profile Page - Update user and profile information
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # → Allows the user to edit their username, email, and profile picture

    # Prediction History Page - View all past predictions
    path('profile/history/', views.prediction_history, name='prediction_history'),
    # → Shows the list of past skin predictions uploaded by the logged-in user

    # Individual Prediction Result Page
    path('prediction/<int:prediction_id>/', views.prediction_result, name='prediction_result'),
    # → Displays the result for a specific prediction based on the given ID
    # → Includes disease name, confidence, and additional information

    # Disease Detail Page - Static info based on predicted disease name
    path('disease/<str:disease_name>/', views.disease_detail, name='disease_detail'),
    # → Provides detailed info like symptoms, causes, treatments for a particular disease
    # → Data is pulled from a static dictionary or file

    # Change Password Page using built-in Django view
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='detection/change_password.html',  # Custom template
            success_url='/profile/'  # Redirect to profile after successful password change
        ),
        name='change_password'
    ),
]

