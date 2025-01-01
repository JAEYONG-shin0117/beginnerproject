from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import UploadedFile

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'jpg', 'png','pdf','doc','docx']

def validate_file_extension(file):
    """파일 확장자 검증"""
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ParseError(f"Unsupported file extension: {ext}")

class FileUploadView(APIView):
    def post(self, request):
        # 요청에 파일이 포함되어 있는지 확인
        if 'file' not in request.FILES:
            raise ParseError("No file attached")

        # 파일 가져오기 및 검증
        file = request.FILES['file']
        validate_file_extension(file)

        # 파일 저장
        uploaded_file = UploadedFile.objects.create(file=file)

        # 저장된 파일의 URL 반환
        return Response({
            'file_url': uploaded_file.file.url,
            'message': 'File uploaded successfully'
        })
