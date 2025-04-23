from django.contrib import admin
from .models import Profile, SkinImage, SkinPrediction

# ---------------------------------------------
# Admin configuration for the Profile model
# ---------------------------------------------
class ProfileAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('user', 'profile_pic')

# ---------------------------------------------
# Admin configuration for the SkinImage model
# ---------------------------------------------
class SkinImageAdmin(admin.ModelAdmin):
    # Fields to show in the list view of the SkinImage model
    list_display = ('prediction', 'uploaded_at')

    # Make 'uploaded_at' field read-only in the admin panel
    # So it can't be changed manually
    readonly_fields = ('uploaded_at',)

# ---------------------------------------------
# Admin configuration for the SkinPrediction model
# ---------------------------------------------
class SkinPredictionAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('user', 'prediction', 'confidence', 'uploaded_at')

    # Make 'uploaded_at' read-only to prevent accidental edits
    readonly_fields = ('uploaded_at',)

# ---------------------------------------------
# Register the models and their admin configurations
# ---------------------------------------------
admin.site.register(Profile, ProfileAdmin)              # Register Profile model with custom admin
admin.site.register(SkinImage, SkinImageAdmin)          # Register SkinImage model with custom admin
admin.site.register(SkinPrediction, SkinPredictionAdmin)  # Register SkinPrediction model with custom admin
