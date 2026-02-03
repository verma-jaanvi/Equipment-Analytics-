from django.http import FileResponse
from django.shortcuts import get_object_or_404
import os

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from .models import DatasetUpload
from .analytics import analyze_csv
from .serializers import DatasetUploadSerializer
from .report import generate_pdf


# ============================================================
# ✅ CSV Upload Endpoint
# ✅ Per User Upload + Auto Cleanup (Keep Last 5 Only)
# ============================================================

class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response({"error": "CSV file is required"}, status=400)

        # ✅ Save dataset linked to current logged-in user
        dataset = DatasetUpload.objects.create(
            user=request.user,
            file=file,
            filename=file.name,
            summary={}
        )

        # ✅ Analyze CSV file
        summary = analyze_csv(dataset.file.path)

        # ✅ Save analysis summary in DB
        dataset.summary = summary
        dataset.save()

        # =====================================================
        # ✅ DATA HANDLING REQUIREMENT
        # Keep ONLY last 5 uploads per user
        # Delete older datasets + files + reports
        # =====================================================

        uploads = DatasetUpload.objects.filter(
            user=request.user
        ).order_by("-uploaded_at")

        if uploads.count() > 5:
            old_uploads = uploads[5:]  # everything older than latest 5

            for old in old_uploads:

                # ✅ Delete CSV file from disk
                if old.file and os.path.isfile(old.file.path):
                    os.remove(old.file.path)

                # ✅ Delete old PDF report if generated earlier
                pdf_path = f"uploads/report_{old.id}.pdf"
                if os.path.isfile(pdf_path):
                    os.remove(pdf_path)

                # ✅ Finally delete DB row
                old.delete()

        return Response({
            "message": "File uploaded successfully ✅",
            "dataset_id": dataset.id,
            "summary": summary
        })


# ============================================================
# ✅ History API Endpoint (Per User)
# Returns last 5 uploads for current user
# ============================================================

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        datasets = DatasetUpload.objects.filter(
            user=request.user
        ).order_by("-uploaded_at")[:5]

        serializer = DatasetUploadSerializer(datasets, many=True)
        return Response(serializer.data)


# ============================================================
# ✅ Report Endpoint (User Protected)
# User can download ONLY their own dataset report
# ============================================================

class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):

        dataset = get_object_or_404(
            DatasetUpload,
            id=dataset_id,
            user=request.user
        )

        # ✅ Generate report path
        pdf_path = f"uploads/report_{dataset_id}.pdf"

        # ✅ Generate PDF report
        generate_pdf(dataset, pdf_path)

        return FileResponse(
            open(pdf_path, "rb"),
            as_attachment=True,
            filename=f"report_{dataset_id}.pdf"
        )


# ============================================================
# ✅ Signup Endpoint (SQLite Auth)
# Creates new user securely (password hashed)
# ============================================================

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        # ✅ Validation
        if not username or not email or not password:
            return Response({"error": "All fields are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        # ✅ Correct secure user creation
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({"success": "User created successfully ✅"})