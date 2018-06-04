from django.db import models


class MyIntData(models.Model):
    name = models.CharField(max_length=10)
    content = models.TextField(blank=False)

    def __str__(self):
        return self.name

class MyColData(models.Model):
    name = models.CharField(max_length=10)
    content = models.TextField(blank=False)

    def __str__(self):
        return self.name

class UserInfo(models.Model):
    user_name = models.CharField(max_length=10)
    user_int = models.CharField(max_length=10)
    user_col = models.CharField(max_length=10)

    def __str__(self):
        return self.user_name
