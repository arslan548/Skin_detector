# ---------------------------------------------
# Django Forms for Skin Disease Detector App
# ---------------------------------------------

from django import forms
from .models import SkinImage, SkinPrediction, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# -------------------------------
# UpdateUserForm
# -------------------------------
# This form allows users to update basic user model info
class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)  # Make first name required
    last_name = forms.CharField(required=True)   # Make last name required
    email = forms.EmailField(required=True)      # Make email required

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


# -------------------------------
# UpdateProfileForm
# -------------------------------
# This form is used to update the user’s profile picture
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']


# -------------------------------
# RegisterForm
# -------------------------------
# Custom user registration form with password confirmation
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)           # Password field with hidden input
    confirm_password = forms.CharField(widget=forms.PasswordInput)   # Confirmation field for password

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    # Validate that both password fields match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")


# -------------------------------
# LoginForm
# -------------------------------
# Custom login form extending Django’s built-in AuthenticationForm
class LoginForm(AuthenticationForm):
    username = forms.CharField()                          # Username input
    password = forms.CharField(widget=forms.PasswordInput)  # Password input


# -------------------------------
# SkinImageForm
# -------------------------------
# Form for uploading an image for prediction
class SkinImageForm(forms.ModelForm):
    class Meta:
        model = SkinImage
        fields = ['image']  # Only upload image field


# -------------------------------
# SkinPredictionForm
# -------------------------------
# Form for uploading an image and storing predictions (with confidence)
class SkinPredictionForm(forms.ModelForm):
    class Meta:
        model = SkinPrediction
        fields = ['image']  # Only the image is needed from the user


# -------------------------------
# EditProfileForm
# -------------------------------
# A simpler form for editing only the email of the user
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']


# -------------------------------
# ProfilePictureForm
# -------------------------------
# Separate form to update only the profile picture
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']
