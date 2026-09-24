from django.db import models


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "Usuario"),
        ("assistant", "Asistente"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
