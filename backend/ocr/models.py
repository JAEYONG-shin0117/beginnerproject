import os
from uuid import uuid4
from django.db import models

def upload_to(instance, filename):
    """파일 저장 경로와 고유 파일 이름 생성"""
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid4().hex}.{ext}"  # 고유한 파일 이름 생성
    return os.path.join('uploads/', unique_filename)

class UploadedFile(models.Model):
    file = models.FileField(upload_to=upload_to)  # 커스텀 저장 경로 사용
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 업로드 시간 자동 저장

    def __str__(self):
        return self.file.name
