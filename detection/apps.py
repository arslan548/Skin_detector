from django.apps import AppConfig

# ----------------------------------------------
# App Configuration Class for the 'detection' App
# ----------------------------------------------
class DetectionConfig(AppConfig):
    # Specifies the default field type to use for auto-generated primary keys.
    # 'BigAutoField' creates a 64-bit integer instead of the default 32-bit.
    default_auto_field = 'django.db.models.BigAutoField'

    # Name of the app this configuration belongs to
    name = 'detection'

    # ----------------------------------------------
    # The ready() method is called when the app is loaded.
    # This is a good place to import and connect signals.
    # ----------------------------------------------
    def ready(self):
        # Import signal handlers so they are registered with Django
        # When a User is created or updated, the associated profile is created/updated too.
        import detection.signals
