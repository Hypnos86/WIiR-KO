from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from units.models import Unit


@receiver(pre_save, sender=Unit)
def create_unit_fields(sender, instance, **kwargs):
    instance.unit_full_name = f'{instance.type.type_full} {instance.city} - {instance.address}'
    text = f'{instance.type.type_short} {instance.city} {instance.address} {instance.id}'

    if instance.slug != text:
        instance.slug = slugify(text, )


@receiver(post_save, sender=Unit)
def edit_slug(sender, instance, created, **kwargs):
    if "none" in instance.slug:
        text = f'{instance.type.type_short} {instance.city} {instance.address} {instance.id}'
        instance.slug = slugify(text, )
        instance.save()
