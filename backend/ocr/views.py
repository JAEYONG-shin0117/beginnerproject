import os
import pytesseract
import pdfplumber
import nltk
from PIL import Image, UnidentifiedImageError
from transformers import pipeline
from rake_nltk import Rake
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import UploadedFile

# NLTK 데이터 경로 설정
nltk.data.path.append('C:/Users/sjyss/nltk_data')

ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']  # 허용되는 파일 확장자


def validate_file_extension(file):
    """파일 확장자 검증"""
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ParseError(f"지원하지 않는 파일 형식입니다: {ext}")


def clean_text(text):
    """텍스트 전처리: 특수 문자 및 공백 제거"""
    import re
    text = re.sub(r'\s+', ' ', text)  # 다중 공백 제거
    text = re.sub(r'[^\w\s.,]', '', text)  # 특수 문자 제거
    text = re.sub(r'[,]+', ',', text)  # 중복된 쉼표 제거
    text = text.replace("\n", " ")  # 줄바꿈 제거
    return text.strip()


def chunk_text(text, chunk_size=512):
    """텍스트를 지정된 길이로 나누는 함수"""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size]).strip()
        if len(chunk.split()) >= 30:  # 최소 30단어 이상인 청크만 처리
            yield chunk


class FileUploadView(APIView):
    def post(self, request):
        # 파일 요청 확인
        if 'file' not in request.FILES:
            return Response({'error': '파일이 포함되어 있지 않습니다.'}, status=400)

        # 파일 가져오기 및 확장자 검증
        file = request.FILES['file']
        validate_file_extension(file)

        # 파일 저장
        uploaded_file = UploadedFile.objects.create(file=file)
        file_path = default_storage.save(uploaded_file.file.name, file)
        absolute_path = default_storage.path(file_path)

        # 파일 유형별 처리
        ext = file.name.split('.')[-1].lower()
        extracted_text = ""

        try:
            if ext in ['jpg', 'jpeg', 'png']:
                # 이미지 OCR 처리
                extracted_text = pytesseract.image_to_string(Image.open(absolute_path))
            elif ext == 'pdf':
                # PDF 텍스트 추출
                with pdfplumber.open(absolute_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text += page_text + "\n"
            else:
                raise ParseError(f"지원하지 않는 파일 형식입니다: {ext}")
        except UnidentifiedImageError:
            return Response({'error': '이미지 파일을 처리할 수 없습니다.'}, status=400)
        except Exception as e:
            return Response({'error': f"파일 처리 중 문제가 발생했습니다: {str(e)}"}, status=500)

        # 텍스트 전처리
        extracted_text = clean_text(extracted_text)
        if not extracted_text:
            return Response({'error': '파일에서 텍스트를 추출할 수 없습니다.'}, status=400)

        # 텍스트 요약
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        chunks = list(chunk_text(extracted_text, chunk_size=512))
        if not chunks:
            return Response({'error': '추출된 텍스트가 요약에 충분하지 않습니다.'}, status=400)

        summaries = []
        failed_chunks = []
        for idx, chunk in enumerate(chunks):
            try:
                summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                failed_chunks.append({'chunk_index': idx, 'chunk_text': chunk, 'error': str(e)})

        final_summary = " ".join(summaries)

        # 키워드 추출
        rake = Rake()
        rake.extract_keywords_from_text(extracted_text)
        keywords = rake.get_ranked_phrases()[:10]

        # 응답 반환
        return Response({
            'file_url': uploaded_file.file.url,
            'extracted_text': extracted_text,
            'summary': final_summary if summaries else "요약 결과가 없습니다.",
            'failed_chunks': failed_chunks,  # 요약 실패한 청크 정보
            'keywords': keywords,
            'message': '텍스트 추출 및 요약이 성공적으로 완료되었습니다.'
        })

