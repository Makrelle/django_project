from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

class Address(models.Model):
    street = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

class Company(models.Model):
    # tuple, ale muze byt i list
    status_choices = (
        ("N", "New"),
        ("L", "Lead"),
        ("O", "Opportunity"),
        ("C", "Active Customer"),
        ("FC", "Former Customer"),
        ("I", "Inactive")
    )
    name = models.CharField(_("Name"), max_length=50)
    status = models.CharField(_("Status"), max_length=2, default="N", choices=status_choices)
    # maxlength delka te zkratky,
    phone_number = models.CharField(_("Phone number"), max_length=20, null=True, blank=True)
    # nemusi byt zadan email, aby se dalo ulozit
    email = models.CharField(max_length=50, null=True, blank=True)
    identification_number = models.CharField(max_length=100)
    # radeji jako string, aby se napr. neodmazaly nuly na zacatku
    address = models.ForeignKey("Address", on_delete=models.SET_NULL, null=True, blank=True)

class Contact(models.Model):
    primary_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    # vzdycky musi byt, co se stane, kdyz se smaze
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)


class Opportunity(models.Model):
    status_choices = (
        ("1", "Prospecting"),
        ("2", "Analysis"),
        ("3", "Proposal"),
        ("4", "Negotiation"),
        ("5", "Closed Won"),
        ("0", "Closed Lost"),
    )
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    sales_manager = models.ForeignKey(User, on_delete=models.RESTRICT)
    primary_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, default="1", choices=status_choices)
    obchodni_pripad = models.DecimalField(max_digits=6, decimal_places=2, default=0.45)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    office_number = models.CharField(max_length=20, blank=True, null=True)
    manager = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=Opportunity)
def create_opportunity(sender, instance, created, **kwargs):
    if created:
        send_mail("New Opportunity", "instance", "robot@mojefirma.cz", ["sales_manager@czechitas.cz"])




