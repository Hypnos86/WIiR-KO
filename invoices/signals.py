from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from invoices.models import Invoice


@receiver(post_save, sender=Invoice)
def create_slug(sender, instance, **kwargs):
    slug_text = f'{instance.no_invoice}-{instance.id}'
    if not instance.slug:
        instance.slug = slugify(slug_text, )
        instance.save()

