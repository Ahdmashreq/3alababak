from django.db import models


class UomCategoryManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(UomCategoryManager, self).filter(company=user.company)


class UomManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(UomManager, self).filter(company=user.company)



class LocationManager(models.Manager):
    def all(self, user, *args, **kwargs):
        return super(LocationManager, self).filter(company=user.company)
