from django.db import models


class User(models.Model):
    email = models.EmailField(verbose_name='Электронная почта')
    last_name = models.CharField(verbose_name='Фамилия', max_length=256)
    first_name = models.CharField(verbose_name='Имя', max_length=256)
    middle_name = models.CharField(verbose_name='Отчество', max_length=256)
    phone = models.CharField(verbose_name='Номер телефона', max_length=11)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота над уровнем моря')

    def __str__(self):
        return f"Coords({self.latitude}, {self.longitude}, {self.height})"

class Levels(models.Model):
    level_spring = models.CharField(verbose_name='Уровень сложности весной', max_length=5, blank=True)
    level_summer = models.CharField(verbose_name='Уровень сложности летом', max_length=5, blank=True)
    level_autumn = models.CharField(verbose_name='Уровень сложности осенью', max_length=5, blank=True)
    level_winter = models.CharField(verbose_name='Уровень сложности зимой', max_length=5, blank=True)

    def __str__(self):
        return f"Levels(Spring: {self.level_spring}, Summer: {self.level_summer}, Autumn: {self.level_autumn}, Winter: {self.level_winter})"


class Pereval(models.Model):
    NEW, PENDING, ACCEPTED, REJECTED = 'NE', 'PE', 'AC', 'RE'
    STATUS_CHOICES = [
        (NEW, 'new'),
        (PENDING, 'pending'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected')
    ]
    status = models.CharField(verbose_name='Статус', max_length=2, choices=STATUS_CHOICES, default=NEW)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    levels = models.OneToOneField(Levels, on_delete=models.CASCADE)
    beauty_title = models.CharField(verbose_name='Тип местности', max_length=256)
    title = models.CharField(verbose_name='Название', max_length=256)
    other_titles = models.CharField(verbose_name='Другие названия', max_length=256)
    connect = models.TextField(verbose_name='Сопроводительный текст', blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pereval({self.title}, Status: {self.get_status_display()})"

class Image(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
    data = models.URLField()
    title = models.CharField(verbose_name='Примечание', max_length=256, blank=True)
    datetime = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Image({self.title}) for {self.pereval.title}"
