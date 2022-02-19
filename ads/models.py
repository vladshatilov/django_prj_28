from django.db import models


class City(models.Model):
    STATUSES = [("open", "Open"), ("closed", "Closed")]

    name = models.CharField(max_length=50)
    status = models.CharField(max_length=6, choices=STATUSES, default="open")

    class Meta:
        ordering = ["name"]
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class User(models.Model):
    ROLES = [('member', "Member"), ("admin", "Admin")]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLES, default='member')
    age = models.PositiveSmallIntegerField(blank=True)
    locations = models.ManyToManyField(City)

    class Meta:
        ordering = ["username"]
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'

    def __str__(self):
        return self.username


class Ads(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    author_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    author = models.CharField(max_length=150, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    poster = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ["-price"]
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ["name"]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
