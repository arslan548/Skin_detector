# ------------------------------------------------------------
# Django Signal to Automatically Create/Update Profile Model
# ------------------------------------------------------------

# Import necessary modules to handle Django signals and user model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile  # Import the custom Profile model

# ------------------------------------------------------------
# Signal Receiver: Automatically creates or updates Profile
# whenever a User instance is created or saved
# ------------------------------------------------------------

@receiver(post_save, sender=User)  # Connect this function to the post_save signal of the User model
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Signal that listens for the 'post_save' event on the User model.

    If a new User is created, it will also create an associated Profile.
    If an existing User is updated, it will save the associated Profile.
    """
    if created:
        # If the User instance is newly created, create a corresponding Profile instance
        Profile.objects.create(user=instance)

    # In both cases (created or updated), ensure the Profile is saved
    instance.profile.save()
