from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import pre_save
from .models import user_wallet

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




@receiver(pre_save, sender=user_wallet)
def wallet_updated(sender, instance, **kwargs):

    if not instance.pk:
        # New wallet being created
        return

    try:
        old_wallet = user_wallet.objects.get(pk=instance.pk)
    except user_wallet.DoesNotExist:
        return

    old_balance = Decimal(old_wallet.total_balance)
    new_balance = Decimal(instance.total_balance)

    if old_balance == new_balance:
        return

    if new_balance > old_balance:
        amount_added = new_balance - old_balance

        subject = "Funds Credited Successfully"

        text_content = f"""
Dear {instance.user.first_name},

Your account has been credited successfully.

Amount Credited: ${amount_added:,.2f}

Available Balance: ${new_balance:,.2f}

Thank you for banking with us.
"""

        html_content = f"""
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f5f8fc;font-family:Arial,sans-serif;">

<table width="100%" style="padding:40px;background:#f5f8fc;">
<tr>
<td align="center">

<table width="600" style="background:#fff;border-radius:10px;overflow:hidden;">

<tr>
<td style="background:#0d6efd;padding:30px;text-align:center;">
<h2 style="color:#fff;margin:0;">Funds Received</h2>
</td>
</tr>

<tr>
<td style="padding:40px;">

<h3>Hello {instance.user.first_name},</h3>

<p>Your account has been credited successfully.</p>

<div style="background:#eef5ff;padding:20px;border-left:5px solid #0d6efd;margin:25px 0;">

<p><strong>Amount Credited</strong></p>

<h2 style="color:#0d6efd;">
${amount_added:,.2f}
</h2>

<p><strong>Available Balance</strong></p>

<h2 style="color:#198754;">
${new_balance:,.2f}
</h2>

</div>

<p>
Thank you for banking with us.
</p>

</td>
</tr>

<tr>
<td style="background:#0d6efd;color:#fff;padding:18px;text-align:center;">
© 2026 Your Bank
</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)