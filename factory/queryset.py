from django.utils import timezone
from django.db import models

class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

    def today(self):
        t = timezone.localtime(timezone.now())
        today = self.filter(created_at__year = t.year,
            created_at__month = t.month, created_at__day = t.day, )
        return today
