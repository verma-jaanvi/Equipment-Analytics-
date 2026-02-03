from django.db import models
from django.contrib.auth.models import User


class DatasetUpload(models.Model):
    # ✅ NEW: Link dataset upload to a user (per-user history)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,        # ✅ keeps old records safe
        blank=True
    )

    # ✅ Uploaded dataset file (UNCHANGED)
    file = models.FileField(upload_to="datasets/")

    # ✅ Store original filename (UNCHANGED)
    filename = models.CharField(max_length=255)

    # ✅ Summary JSON (UNCHANGED)
    summary = models.JSONField(default=dict)

    # ✅ Upload timestamp (UNCHANGED)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # ✅ Handles uploads even if user is missing (old datasets)
        if self.user:
            return f"{self.user.username} - {self.filename}"
        return f"Dataset {self.id} - {self.filename}"