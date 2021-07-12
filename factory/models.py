from django.db import models
from django.utils import timezone
from .managers import SoftDeletionManager
from django.conf import settings




class FactoryModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)


    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(FactoryModel, self).delete()


