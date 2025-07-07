from django.db import models
from django.conf import settings

author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Post(models.Model):
    CATEGORY_CHOICES = [
        ("diary", "영어일기"),
        ("speaking", "영어회화"),
        ("personal_feedback", "학습점검"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="diary"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # ✅ 수정 완료
    content = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.username}의 댓글"

    def is_reply(self):
        return self.parent is not None
