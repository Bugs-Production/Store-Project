from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    image = models.ImageField('Аватар', upload_to='users_images', blank=True, null=True)
    GENDER_CHOICES = [
        ('N', 'Не выбрано'),
        ('M', 'Мужской'),
        ('G', 'Женский'),
    ]

    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, default='N')
    email_verification = models.BooleanField('Статус верификации', default=False)


class EmailVerification(models.Model):
    class Meta:
        verbose_name = 'верификацию'
        verbose_name_plural = 'Верификация почты'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Верификация для пользователя с {self.user.email}'

    def send_verification_email(self):  # Логика для отправки верификации на почту
        link = reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = (f'Для подтверждения учетной записи {self.user.email} '
                   f'перейдите по ссылке {verification_link}')

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):  # Логика для проверки срока годности ссылки
        return True if now() >= self.expiration else False
