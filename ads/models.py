from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('books', 'Книги'),
        ('clothes', 'Одежда'),
    ]
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('good', 'Хорошее'),
        ('used', 'Б/У'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="proposals_sent")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="proposals_received")
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange from Ad#{self.ad_sender.id} to Ad#{self.ad_receiver.id} ({self.status})"