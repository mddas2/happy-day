# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from root.models import Navigation

@receiver(pre_save, sender=Navigation)
def NavigationPreSave(sender, instance, **kwargs):
    print("")
    
    SetInstance(instance.name,instance , count = 0)

def SetInstance(non_checked_name,instance , count):
    name_obj_count = Navigation.objects.filter(name=non_checked_name).count()
    print(str(name_obj_count)+":"+non_checked_name)

    if name_obj_count > 0:
       non_checked_name = str(instance.name) + "-" +str(name_obj_count+count)
       count = count + 1
       print("checking another one "+ non_checked_name)
       SetInstance(non_checked_name,instance,count)
    else:
        instance.name = non_checked_name
        print("New name found : " + non_checked_name)
        return non_checked_name


   
