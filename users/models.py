from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile_images/user_{0}-{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    other_name = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    cover_img = ResizedImageField(size=[500, 300], quality=100, upload_to=user_directory_path,
                                  default='defaults/avatar.svg', null=True, blank=True)
    is_technician = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        if self.is_technician:
            return f"Technician' {self.first_name} {self.last_name} Profile"
        elif self.is_patient:
            return f"Patient {self.first_name}"
        elif self.is_doctor:
            return f"Doctor {self.first_name}"
        else:
            return f"{self.user.username}'s profile"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def user_role(self):
        if self.is_technician:
            return "technician"
        elif self.is_patient:
            return "patient"
        elif self.is_doctor:
            return "doctor"

#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         print("new_user_instance: ", instance)
#         new_user = UserProfile.objects.create(user=instance, is_technician=True)
#         print("User profile created: ", new_user)
#
#     # try:
#     #     instance.profile.save()
#     # except AttributeError:
#     #     pass
