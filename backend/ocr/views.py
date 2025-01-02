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
import logging

# 로거 설정
logger = logging.getLogger(__name__)

# 허용되는 파일 확장자
ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']

def validate_file_extension(file):
    """파일 확장자 검증"""
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ParseError(f"지원하지 않는 파일 형식입니다: {ext}")

def clean_text(text):
    """텍스트 전처리"""
    import re
    import html
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text)  # 다중 공백 제거
    text = re.sub(r'[^\w\s.,?!]', '', text)  # 특수 문자 제거
    text = re.sub(r'[,]+', ',', text)  # 중복 쉼표 제거
    text = text.replace("\n", " ").replace("\r", " ")  # 줄바꿈 제거
    text = re.sub(r'([.!?])\1+', r'\1', text)  # 반복된 구두점 제거
    return text.strip()

def chunk_text(text, chunk_size=512):
    """텍스트 청크 분리"""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size]).strip()
        if len(chunk.split()) >= 50:  # 최소 50단어 이상인 청크만 처리
            yield chunk

class FileUploadView(APIView):
    def post(self, request):
        # 파일 요청 확인
        if 'file' not in request.FILES:
            logger.debug("No file found in the request.")
            return Response({'error': '파일이 포함되어 있지 않습니다.'}, status=400)

        file = request.FILES['file']

        # 파일 확장자 검증
        try:
            validate_file_extension(file)
        except ParseError as e:
            logger.error(f"Invalid file extension: {e}")
            return Response({'error': str(e)}, status=400)

        # 파일 저장
        uploaded_file = UploadedFile.objects.create(file=file)
        file_path = default_storage.save(uploaded_file.file.name, file)
        absolute_path = default_storage.path(file_path)
        logger.debug(f"File saved at {absolute_path}")

        # 텍스트 추출
        extracted_text = ""
        try:
            if file.name.endswith(('jpg', 'jpeg', 'png')):
                extracted_text = pytesseract.image_to_string(Image.open(absolute_path))
            elif file.name.endswith('pdf'):
                with pdfplumber.open(absolute_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text += page_text + "\n"
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return Response({'error': f"텍스트 추출 중 문제가 발생했습니다: {str(e)}"}, status=500)

        # 전처리 및 검증
        extracted_text = clean_text(extracted_text)
        if not extracted_text:
            logger.warning("No text could be extracted.")
            return Response({'error': '텍스트를 추출할 수 없습니다.'}, status=400)

        # 텍스트 요약
        summarizer = pipeline("summarization", model="google/pegasus-large", tokenizer="google/pegasus-xsum")
        chunks = list(chunk_text(extracted_text, chunk_size=256))
        if not chunks:
            logger.warning("Extracted text is insufficient for summarization.")
            return Response({'error': '추출된 텍스트가 요약에 충분하지 않습니다.'}, status=400)

        summaries, failed_chunks = [], []
        for idx, chunk in enumerate(chunks):
            try:
                input_length = len(chunk.split())
                max_length = min(150, input_length)  # 입력 크기에 따라 max_length 조정
                min_length = max(20, int(max_length * 0.3))  # min_length는 max_length의 30%로 설정

                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                logger.error(f"Summarization failed for chunk {idx}: {e}")
                failed_chunks.append({'chunk_index': idx, 'chunk_text': chunk, 'error': str(e)})

        final_summary = " ".join(summaries) if summaries else "요약 결과가 없습니다."

        # 키워드 추출
        rake = Rake()
        rake.extract_keywords_from_text(extracted_text)
        keywords = [kw.strip() for kw in rake.get_ranked_phrases()[:10]]

        # 응답 반환
        return Response({
            'file_url': uploaded_file.file.url,
            'extracted_text': extracted_text,
            'summary': final_summary,
            'failed_chunks': failed_chunks,
            'keywords': keywords,
            'message': '텍스트 추출 및 요약이 성공적으로 완료되었습니다.'
        })
