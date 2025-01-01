import os
import pytesseract
import pdfplumber
from PIL import Image, UnidentifiedImageError
from transformers import pipeline
from rake_nltk import Rake
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import UploadedFile

ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']  # 허용되는 파일 확장자

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
        file_path = default_storage.save(uploaded_file.file.name, file)
        absolute_path = default_storage.path(file_path)

        # 파일 유형에 따라 처리
        ext = file.name.split('.')[-1].lower()
        extracted_text = ""

        try:
            if ext in ['jpg', 'jpeg', 'png']:
                # 이미지 파일 OCR 처리
                extracted_text = pytesseract.image_to_string(Image.open(absolute_path))
            elif ext == 'pdf':
                # PDF 파일 처리
                with pdfplumber.open(absolute_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text += page_text + "\n"
            else:
                raise ParseError(f"Unsupported file type: {ext}")
        except UnidentifiedImageError:
            return Response({'error': 'Cannot process the uploaded file as an image'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

        if not extracted_text.strip():
            return Response({'error': 'No text could be extracted from the file'}, status=400)

        # 텍스트 요약
        summarizer = pipeline("summarization")
        try:
            summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
        except Exception as e:
            return Response({'error': f"Summarization failed: {str(e)}"}, status=500)

        # 키워드 추출
        rake = Rake()
        rake.extract_keywords_from_text(extracted_text)
        keywords = rake.get_ranked_phrases()[:10]

        return Response({
            'file_url': uploaded_file.file.url,
            'extracted_text': extracted_text.strip(),
            'summary': summary[0]['summary_text'] if summary else "No summary available",
            'keywords': keywords,
            'message': 'File uploaded, text extracted, summarized, and keywords generated successfully.'
        })
