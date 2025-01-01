from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # 파일 저장 경로
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 업로드 시간

    def __str__(self):
        return self.file.name

