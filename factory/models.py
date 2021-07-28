from django.db import models
from django.utils import timezone
from .managers import SoftDeletionManager
from django.conf import settings
from flex.ussd.utils.decorators import export




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


@export()
class QuerySet(models.QuerySet):
    def annotations(self, *args):
        qs = self
        for k in args:
            method = getattr(qs, "annotate_" + str(k))
            qs = method()
        return qs


@export()
class Manager(models.Manager.from_queryset(QuerySet)):
    pass


@export()
class Model(models.Model):

    objects = Manager()

    class Meta:
        abstract = True



class QuerySetChain(object):
    def __init__(self, *args):
        self.querysets = args
        self._count = None

    def count(self):
        if not self._count:
            self._count = sum(qs.count() for qs in self.querysets)
        return self._count

    def __len__(self):
        return self.count()

    def __getitem__(self, item):
        indices = (offset, stop, step) = item.indices(self.count())
        items = []
        total_len = stop - offset
        for qs in self.querysets:
            items += list(qs[offset:stop])
        return items



