import json
import logging

# Django core imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Form and model imports
from .forms import (
    SkinPredictionForm, RegisterForm, LoginForm,
    UpdateUserForm, UpdateProfileForm
)
from .models import SkinPrediction
from .disease_data import disease_details

# Roboflow setup for AI model inference
from roboflow import Roboflow
rf = Roboflow(api_key="yBBBTl63T9D93vxmiWXs")
project = rf.workspace().project("poxclassification")
model = project.version(1).model

# Logger setup
logger = logging.getLogger(__name__)

# ----------------------------- User Registration View -----------------------------
def register_user(request):
    """
    Handle new user registration.
    - If POST: Validate and create new user.
    - If GET: Show empty registration form.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Secure password hash
            user.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = RegisterForm()
    return render(request, 'detection/register.html', {'form': form})


# ----------------------------- User Login View -----------------------------
def login_user(request):
    """
    Handle user login.
    - If POST: Authenticate and log in user.
    - If GET: Show login form.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('upload_image')  # Redirect to image upload page
    else:
        form = LoginForm()
    return render(request, 'detection/login.html', {'form': form})


# ----------------------------- User Logout View -----------------------------
def logout_user(request):
    """
    Logs the current user out and redirects to the login page.
    """
    logout(request)
    return redirect('login')


# ----------------------------- Image Upload & Prediction View -----------------------------
@login_required
def upload_image(request):
    """
    Handle image upload and disease prediction.
    - Uses Roboflow model to predict disease.
    - Saves prediction and confidence in DB.
    """
    if request.method == 'POST':
        form = SkinPredictionForm(request.POST, request.FILES)
        if form.is_valid():
            skin_prediction = form.save(commit=False)
            skin_prediction.user = request.user
            skin_prediction.save()

            prediction = "Normal Skin / No Disease"
            try:
                # Perform prediction using Roboflow model
                result = model.predict(skin_prediction.image.path).json()
                logger.debug(f"Raw prediction result: {result}")

                preds_list = result.get('predictions', [])
                if preds_list and isinstance(preds_list, list) and len(preds_list) > 0:
                    preds_dict = preds_list[0].get('predictions', {})
                    if preds_dict and isinstance(preds_dict, dict):
                        # Select prediction with highest confidence
                        predicted_class, pred_data = max(
                            preds_dict.items(), key=lambda item: item[1].get('confidence', 0)
                        )
                        confidence = float(pred_data.get('confidence', 0))
                        confidence_percent = confidence * 100

                        # Handle Normal vs. Diseased prediction differently
                        if predicted_class.lower() in ['normal skin / no disease', 'healthy']:
                            prediction = f"{predicted_class}"
                            skin_prediction.confidence = confidence_percent
                        else:
                            prediction = f"{predicted_class} (Confidence: {confidence_percent:.0f}%)"
                            skin_prediction.confidence = confidence_percent
                    else:
                        prediction = "Normal Skin / No Disease"
                        skin_prediction.confidence = 0
                else:
                    prediction = "Normal Skin / No Disease"
                    skin_prediction.confidence = 0

            except Exception as e:
                prediction = f"Error: {str(e)}"
                logger.error(f"Prediction error: {str(e)}")

            # Save prediction in the database
            skin_prediction.prediction = prediction
            skin_prediction.save()

            return redirect('prediction_result', prediction_id=skin_prediction.id)
    else:
        form = SkinPredictionForm()

    return render(request, 'detection/upload.html', {'form': form})


# ----------------------------- Prediction Result View -----------------------------
@login_required
def prediction_result(request, prediction_id):
    """
    Displays prediction result and related disease info.
    Extracts disease name and confidence for better UI display.
    """
    prediction = get_object_or_404(SkinPrediction, id=prediction_id, user=request.user)
    logger.debug(f"Prediction string from DB: {prediction.prediction}")

    prediction_text = prediction.prediction
    confidence = getattr(prediction, 'confidence', None)

    # Extract confidence if not already separated
    if confidence is None:
        if ' (' in prediction_text and prediction_text.endswith('%)'):
            disease_name = prediction_text.split(' (')[0]
            confidence_str = prediction_text.split(' (')[1].rstrip('%)')
            try:
                confidence = float(confidence_str)
            except ValueError:
                confidence = None
        else:
            disease_name = prediction_text
            confidence = None
    else:
        disease_name = prediction_text.split(' (')[0] if ' (' in prediction_text else prediction_text

    # Retrieve disease-related details
    details = disease_details.get(disease_name, {
        "causes": "Information not available.",
        "medications": "Information not available.",
        "symptoms": "Information not available.",
        "what_to_do": "Please consult a healthcare professional."
    })

    context = {
        'prediction': prediction,
        'disease_name': disease_name,
        'confidence': confidence,
        'details': details,
    }

    return render(request, 'detection/prediction_result.html', context)


# ----------------------------- Profile View -----------------------------
@login_required
def profile_view(request):
    """
    Display user profile and prediction history.
    Allows user to update profile picture and info.
    """
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    predictions = SkinPrediction.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, 'detection/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'predictions': predictions,
    })


# ----------------------------- Disease Detail View -----------------------------
@login_required
def disease_detail(request, disease_name):
    """
    Show detailed information about a specific disease.
    Fetches user’s prediction history related to the disease.
    """
    prediction = SkinPrediction.objects.filter(
        prediction__icontains=disease_name,
        user=request.user
    ).first()

    details = disease_details.get(disease_name, {
        "causes": "Information not available.",
        "medications": "Information not available.",
        "symptoms": "Information not available.",
        "what_to_do": "Please consult a healthcare professional."
    })

    context = {
        'disease_name': disease_name,
        'prediction': prediction,
        'details': details,
    }

    return render(request, 'detection/disease_detail.html', context)


# ----------------------------- Prediction History View -----------------------------
@login_required
def prediction_history(request):
    """
    Display list of all past predictions for the logged-in user.
    """
    history = SkinPrediction.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'detection/prediction_history.html', {'history': history})


# ----------------------------- Edit Profile View -----------------------------
@login_required
def edit_profile(request):
    """
    Provide form to edit user profile details and profile picture.
    """
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'detection/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
