import datetime
import os.path
import uuid

from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

class CustomQuerySet(QuerySet):
    def delete(self):
        self.update(active=False)

class ActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(active=True)
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

class Undeletable(models.Model):
    active = models.BooleanField(default=True)
    objects = ActiveManager()

    def delete(self, using=None, force=False):
        self.active = False
        self.save()

    class Meta:
        abstract = True



class TaskABC(models.Model):
    PENDING= "P"
    COMPLETE= "C"
    FAILED = "F"
    status_choices = (
        (PENDING, "pending"),
        (COMPLETE, "completed"),
        (FAILED,   "failed"),
    )

    ERROR_KEY = "error"
    MESSAGE_KEY = "message"

    status = models.CharField(max_length=2, choices=status_choices, default=PENDING)
    meta_data= models.JSONField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.status} - {self.title} - {self.created_at}"

    def set_status_successful(self, msg=None):
        if msg:
            self.__class__.objects.filter(id=self.id).update(
                status = self.COMPLETE, meta_data={self.MESSAGE_KEY: msg}
            )
        else:
            self.__class__.objects.filter(id=self.id).update(status=self.COMPLETE)

    def set_status_failed(self, err_msg):
        self.__class__.objects.filter(id=self.id).update(
            status=self.FAILED, meta_data={self.ERROR_KEY: err_msg}
        )

def random_name_setter(instance, file_name):
    name, extension = os.path.splitext(file_name)
    random_name = str((uuid.uuid4()))
    first_path = random_name[0]
    second_path = random_name[0:2]
    year = str(datetime.date.today().year)
    return 'upload_task_files' + '/' +  year + '/' + first_path + '/' + second_path + '/' + name + '_' + random_name[0:8] + extension

class Task(Undeletable, TaskABC):
    IMPORT_TYPE = "import"
    file = models.FileField(upload_to=random_name_setter)
    q_task_id = models.CharField(max_length=255, null=True, blank=True)

    @classmethod
    def build(cls, file, user):
        raise NotImplemented

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="cars/")
    created_at = models.DateTimeField(auto_now_add=True)



