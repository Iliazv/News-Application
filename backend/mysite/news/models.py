from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL

class New(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    text = models.TextField('Текст', max_length=2000)
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение', blank=True)
    view_count = models.IntegerField('Количество просмотров', default=0)
    like_count = models.ManyToManyField(User, verbose_name='Количество лайков', related_name='new_likes', blank=True)
    dislike_count = models.ManyToManyField(User, verbose_name='Количество дизлайков', related_name='new_dislikes', blank=True)

    def total_likes(self):
        return self.like_count.count()
    
    def total_dislikes(self):
        return self.dislike_count.count()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Tag(models.Model):
    TAG_CHOICES = (
        ('политика', 'Политика'),
        ('наука', 'Наука'),
        ('спорт', 'Спорт'),
        ('экономика', 'Экономика'),
        ('религия', 'Религия'),
        ('туризм', 'Туризм'),
        ('технологии', 'Технологии'),
        ('россия', 'Россия'),
        ('общество', 'Общество'),
        ('европа', 'Европа'),
    )

    new = models.ForeignKey(New, verbose_name='Новость', on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(verbose_name='Тег', max_length=30, choices=TAG_CHOICES)

    def __str__(self):
        return self.tag
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'