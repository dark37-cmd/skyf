from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserDetail(models.Model):
    SKUF_TYPE_CHOICES = [
        ('dota', 'Дота-скуф'),
        ('tanko', 'Танко-скуф'),
    ]

    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    skuf_type = models.CharField(max_length=5, choices=SKUF_TYPE_CHOICES)
    photo = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.full_name