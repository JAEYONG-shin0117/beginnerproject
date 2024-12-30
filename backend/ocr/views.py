from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UploadedFile

class FileUploadView(APIView):
    def post(self, request):
        # 사용자가 업로드한 파일을 처리
        file = request.FILES['file']
        uploaded_file = UploadedFile.objects.create(file=file)  # 파일 저장

        # 저장된 파일의 URL을 반환
        return Response({
            'file_url': uploaded_file.file.url,  # 파일 접근 경로
            'message': 'File uploaded successfully'
        })
