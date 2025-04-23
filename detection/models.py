from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ------------------------------------------------------------
# User Profile Model
# ------------------------------------------------------------
class Profile(models.Model):
    # One-to-one relationship with Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile picture for the user, with a default image
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        # This is used to return a readable string representation of the object
        return f"{self.user.username} Profile"


# ------------------------------------------------------------
# Signal to automatically create or update Profile whenever a User is created or updated
# ------------------------------------------------------------
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new Profile if a new User is created
        Profile.objects.create(user=instance)
    # Always save the Profile when the User is saved
    instance.profile.save()


# ------------------------------------------------------------
# Optional model (can be used for future extensions like uploading multiple images)
# Not used in your current codebase but kept for reference
# ------------------------------------------------------------
class SkinImage(models.Model):
    # Image field to store the uploaded skin image
    image = models.ImageField(upload_to='uploads/')

    # Predicted disease name (or normal skin)
    prediction = models.CharField(max_length=255)

    # Timestamp when the image was uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return the prediction result for readability
        return self.prediction


# ------------------------------------------------------------
# Main model to store predictions with user reference
# ------------------------------------------------------------
class SkinPrediction(models.Model):
    # Link the prediction to a registered user (can be null or blank for anonymous entries)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Uploaded image that was used for the prediction
    image = models.ImageField(upload_to='uploads/')

    # Prediction result (disease name or "Normal Skin / No Disease")
    prediction = models.CharField(max_length=255)

    # Confidence score of the prediction (optional)
    confidence = models.FloatField(null=True, blank=True)

    # Automatically add the current date/time when the object is created
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return a readable string combining user and prediction
        return f"{self.user} - {self.prediction}"
