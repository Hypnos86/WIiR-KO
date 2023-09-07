from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models import CountyCard


@receiver(pre_save, sender=CountyCard)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name, )


