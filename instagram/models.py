from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator
# from django.contrib.auth.models import User

# min_length_Validator = MinLengthValidator(3)
# min_length_Validator("he") # forms.ValidationError


class Post(models.Model):
    #   auth.User            장고에서 사용하는 가장 좋은 방법
    # models.GenericIPAddressField   조회수 컨트롤의 용이할듯
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='1')
    message = models.TextField(
        validators=[MinLengthValidator(5)]
    )
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y%m')
    is_public = models.BooleanField(default=False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"Custom Post object ({self.id})"
        return self.message

    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    # limit_choices_to = {'is_public': True})
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
