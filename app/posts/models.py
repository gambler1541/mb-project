import re

from django.contrib.auth import get_user_model
from django.db import models



User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    photo = models.ImageField(
        '사진',
        upload_to='post'
    )
    created_at = models.DateTimeField(auto_now_add=True,)
    modified_at = models.DateTimeField(auto_now=True,)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(?P<tag>\w+)')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='포스트',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    content = models.TextField(
        '댓글 내용'
    )
    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='해시태그 목록',
    )

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        # DB에 변경내역ㅇ르 기록한 상태
        super().save(*args, **kwargs)

        # DB에 Comment저장이 완료된 후,
        #   자신의 'content'값에서 해시태그 목록을 가져와서
        #   자신의 'tags'속성 (MTM필드)에 할당
        tags = [HashTag.objects.get_or_create(name=name)[0]
                for name in re.findall(self.TAG_PATTERN, self.content)]
        self.tags.set(tags)


class HashTag(models.Model):
    name = models.CharField(
        '태그명',
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'
