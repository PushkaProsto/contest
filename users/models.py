from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.contenttypes.models import ContentType
from contest import settings
from django.utils.text import slugify
from django.urls import reverse
# group = Group.objects.create(name='Teachers')
# permission = Permission.objects.get(codename='can_create_task')
# group.permissions.add(permission)

class User(AbstractUser):
    choice = models.CharField(("status"), max_length=150, blank=True)
    date = models.DateField(null=True, blank=True)
    slug = models.SlugField(null=False, blank=True, unique=True)
    prepopulated_fields = {'slug': ('username',)}
    class Meta:
        permissions = (("can_create_task", "Can create task"),)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        if self.choice == '3':
            # assign permission to manage users
            self.is_staff = True 
            self.is_superuser = True           
           
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("mydetail", kwargs={"slug": self.slug})    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'



