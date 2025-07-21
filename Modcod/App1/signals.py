from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Logs, CustomUser, Project, Reclamation
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .middleware import CurrentUserMiddleware

User = get_user_model()

def create_log(action, instance, message):
    user = CurrentUserMiddleware.get_current_user()
    if user and user.is_authenticated:
        log_user = user
    else:
        try:
            log_user = User.objects.get(username="system")
        except User.DoesNotExist:
            log_user = None

    if log_user:
        Logs.objects.create(
            user=log_user,
            action=action,
            description=message,
            date_creation=now()
        )
    else:
        pass

@receiver(post_save, sender=CustomUser)
def log_user_create_update(sender, instance, created, **kwargs):
    action = "Create" if created else "Update"
    msg = f"Utilisateur '{instance.username}' a été {'créé' if created else 'modifié'}."
    create_log(action, instance, msg)

@receiver(post_delete, sender=CustomUser)
def log_user_delete(sender, instance, **kwargs):
    msg = f"Utilisateur '{instance.username}' a été supprimé."
    create_log("Delete", instance, msg)

@receiver(post_save, sender=Project)
def log_project_create_update(sender, instance, created, **kwargs):
    action = "Create" if created else "Update"
    msg = f"Projet ID {instance.id} a été {'créé' if created else 'modifié'}."
    create_log(action, instance, msg)

@receiver(post_delete, sender=Project)
def log_project_delete(sender, instance, **kwargs):
    msg = f"Projet ID {instance.id} a été supprimé."
    create_log("Delete", instance, msg)

@receiver(post_save, sender=Reclamation)
def log_reclamation_create_update(sender, instance, created, **kwargs):
    action = "Create" if created else "Update"
    msg = f"Réclamation '{instance.référence}' créée par {instance.username}." if created else f"Réclamation '{instance.référence}' modifiée par {instance.username}."
    create_log(action, instance, msg)

@receiver(post_delete, sender=Reclamation)
def log_reclamation_delete(sender, instance, **kwargs):
    msg = f"Réclamation '{instance.référence}' supprimée par {instance.username}."
    create_log("Delete", instance, msg)
