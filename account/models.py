from django.contrib.auth.models import AbstractUser
from django.db import models
from root.models import MemberShipType

class CustomUser(AbstractUser):    
    phone = models.CharField(max_length=255 , null=True)
    permanent_address = models.CharField(max_length=255 , null=True)
    current_address = models.CharField(max_length=255 , null=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.EmailField(max_length=255, unique=False)  
    apply_role_type = models.IntegerField(null=True) 
    image = models.ImageField(upload_to='user/profile', null=True)
    c_id = models.BigIntegerField(null=True)

    membership = models.ForeignKey(MemberShipType,related_name="users",on_delete=models.CASCADE,null=True)

    SUPERADMIN = 1
    ADMIN = 2
    STAFF = 3
    USER = 4

    ROLE_CHOICES = (
        (SUPERADMIN, 'SUPERADMIN'),
        (ADMIN, 'ADMIN'),
        (STAFF, 'STAFF'),
        (USER, 'USER'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def getRoleName(self):
        if self.role==1:
            return 'SUPERADMIN'
        elif self.role==2:
            return 'ADMIN'
        elif self.role==3:
            return 'STAFF'
        else:
            return 'None'

