import stripe
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, m2m_changed, post_save, pre_delete
from django.dispatch import receiver

from .models import Item, Order, Tax, Discount


@receiver(m2m_changed, sender=Order.items.through)
def validate_model(sender, instance, action, **kwargs):
    """
    A signal receiver function that is triggered when the "items" field of the "Order" model's many-to-many relationship
     is changed. Checks that the Order contains items only one currency.
    Args:
        instance (Order): The instance of the "Order" model that triggered the signal.
    Raises:
        ValidationError: If the currencies of the goods in the "Order" do not match.
    Returns:
        None
    """
    if instance.items.first():
        currency = instance.items.first().currency
        item_currencies = Item.objects.filter(pk__in=kwargs['pk_set']).values_list('currency', flat=True)
        if any(currency != item_currency for item_currency in item_currencies):
            raise ValidationError('The currencies of goods in Order should not differ')


@receiver(post_save, sender=Tax)
def save_tax(sender, instance: Tax, **kwargs):
    """
    Save a tax object and generate a tax hash if it doesn't exist. If tax_hash does not exist, creates Tax on Stripe
    and the result is tax_hash.

    Parameters:
        instance (Tax): The tax object to be saved.
    Returns:
        None
    """
    if instance.tax_hash is None:
        print(instance.tax_hash is None)
        stripe_hash = stripe.TaxRate.create(
            display_name=instance.display_name,
            description=instance.description,
            percentage=instance.percentage,
            inclusive=instance.inclusive,
            active=instance.active,
        )
        instance.tax_hash = stripe_hash.id
        instance.save(update_fields=['tax_hash'])


@receiver(pre_save, sender=Tax)
def update_tax(sender: Tax, instance: Tax, **kwargs):
    """
    Update a tax rate in the Stripe API.
    Args:
        instance (Tax): The tax instance to update.
    Returns:
        None
    """
    if instance.pk is not None:
        stripe.TaxRate.modify(
            instance.tax_hash,
            display_name=instance.display_name,
            description=instance.description,
            active=instance.active
        )


@receiver(pre_delete, sender=Tax)
def delete_tax(sender: Tax, instance: Tax, **kwargs):
    """
    Delete a tax rate in database. On Stripe, changes the Tax status to archive.
    Args:
        instance (Tax): The tax instance to be deleted.
    Returns:
        None
    """
    stripe.TaxRate.modify(
        instance.tax_hash,
        active=False
    )


@receiver(post_save, sender=Discount)
def create_disc(sender: Discount, instance: Discount, **kwargs):
    """
    If discount_hash does not exist, it creates a Coupon on Stripe and stores its id in discount_hash.
    Args:
        instance (Discount): The Discount instance being saved.
    Returns:
        None
    """
    if instance.discount_hash is None:
        stripe_hash = stripe.Coupon.create(
            percent_off=instance.percent_off,
            duration='forever'
        )
        instance.discount_hash = stripe_hash.id
        instance.save(update_fields=['discount_hash'])


@receiver(pre_delete, sender=Discount)
def delete_disc(sender: Discount, instance: Discount, **kwargs):
    """
       Delete a discount from the Stripe API.
       Args:
           instance (Discount): The instance of the discount being deleted.
       Returns:
           None
    """
    stripe.Coupon.delete(instance.discount_hash)
