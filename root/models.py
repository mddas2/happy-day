from django.db import models
from django.conf import settings
from django.contrib.humanize.templatetags import humanize
from datetime import datetime, timedelta
from django.utils import timezone 
from account.models import CustomUser


# Create your models here.
class PageType(models.Model):
    page_name =  models.CharField(max_length=255)  
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return "{page_name:"+self.page_name+","+"status:"+str(self.status)+"}"

class Navigation(models.Model):
    parent = models.ForeignKey('self', related_name="childs",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    parent_page_id = models.IntegerField(default=0)
    caption = models.CharField(max_length=255 , null=True)
    status = models.BooleanField(default=True)
    page_type = models.CharField(max_length=255,null=False,default=False)
    title = models.CharField(max_length=500,null=True)
    short_description = models.CharField(max_length=3000, null=True)
    long_contents = models.TextField(max_length=255,null=True)
    meta_title = models.CharField(max_length=255,null=True)
    keyword = models.CharField(max_length=255,null=True)
    position = models.IntegerField()
    banner_image1 = models.ImageField(upload_to='navigation/banner1', null=True)
    banner_image2 = models.ImageField(upload_to='navigation/banner2', null=True)
    icon_image = models.ImageField(upload_to='navigation/icon', null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    @property
    def getBannerImage1(self):
        if self.banner_image1 :
            return self.banner_image1.url
        return ''

class HomeNavigation(models.Model):
    # product = models.ForeignKey('Products',on_delete=models.CASCADE,null=True)
    parent = models.ForeignKey('self', related_name="childs",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    parent_page_id = models.IntegerField(default=0)
    caption = models.CharField(max_length=255 , null=True)
    status = models.BooleanField(default=True)
    page_type = models.CharField(max_length=255,null=False,default=False)
    title = models.CharField(max_length=500,null=True)
    short_description = models.CharField(max_length=3000, null=True)
    long_contents = models.TextField(max_length=255,null=True)
    meta_title = models.CharField(max_length=255,null=True)
    keyword = models.CharField(max_length=255,null=True)
    position = models.IntegerField()
    banner_image1 = models.ImageField(upload_to='home/banner1', null=True)
    banner_image2 = models.ImageField(upload_to='home/banner2', null=True)
    icon_image = models.ImageField(upload_to='home/icon', null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    @property
    def getBannerImage1(self):
        if self.banner_image1 :
            return self.banner_image1.url
        return ''

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Navigation,related_name="product",on_delete=models.CASCADE,null=True)
    sub_category = models.ForeignKey(Navigation,related_name="product_subcat",on_delete=models.CASCADE,null=True)
    price = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    str_choice = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)]
    star = models.CharField(max_length=50,choices=str_choice,default=0)
    vendor = models.CharField(max_length=255,null=True)
    payment_type = models.CharField(max_length=255,default="COD")
    size =models.CharField(max_length=255,default="medium")
    color =models.CharField(max_length=255,default="white")
    title = models.CharField(max_length=2000,null=True)
    discription = models.TextField(max_length=5000,null=True)   #overview
    long_contents = models.TextField(max_length=5000,null=True) #more
    meta_title = models.CharField(max_length=300,null=True)
    keyword = models.CharField(max_length=2000,null=True)
    brand = models.CharField(max_length=2000,null=True)
    status = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to='uploads/', null=True)
    image2 = models.ImageField(upload_to='uploads/', null=True)
    image3 = models.ImageField(upload_to='uploads/', null=True)
    image4 = models.ImageField(upload_to='uploads/', null=True)
    image5 = models.ImageField(upload_to='uploads/', null=True)
    image6 = models.ImageField(upload_to='uploads/', null=True)
    image7 = models.ImageField(upload_to='uploads/', null=True)
    image8 = models.ImageField(upload_to='uploads/', null=True)
    image9 = models.ImageField(upload_to='uploads/', null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    ftn_choice = [("f","featured"),("t","trending"),("n","new_arrival")]
    ftn = models.CharField(max_length=50,choices=ftn_choice,default="n")

    b2b_membership_price = models.IntegerField(null=True,default=0)
    platinum_membership_price = models.IntegerField(null=True,default=0)
    free_membership_price = models.IntegerField(null=True,default=0)

    membership_type = (
        ('b2b_membership','Business To Business Membership',1),
        ('platinum','Platinum Membership',2),
        ('free','Free Membership',3),
    )

    def __str__(self):
        return "{name:"+self.name+","+"Prpduct_id"+str(self.id)+"}"
    
    def is_hot(self):
        time_difference = timezone.now() - self.created_at
        if time_difference <= timedelta(days=2):
            return 'hot'
        elif time_difference <= timedelta(days=4):
            return 'new'
        elif time_difference <= timedelta(days=6):
            return 'sale'
        else:
            return ''

class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to='excel')
    updated_at = models.DateTimeField(auto_now=True,null=True)


class Order(models.Model):
    # product_id = models.IntegerField(default=0)
    
    product = models.ForeignKey(Products,related_name="order",on_delete=models.CASCADE,null=True)
    product_details = models.TextField(max_length=5000)
    user_id = models.IntegerField(null=False)
    email = models.CharField(max_length=300,null=True)
   
    
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    phone = models.CharField(max_length=25,null=True)
    pdc = models.CharField(max_length=10,null=True) # p>pending , d=delivered , c=cancled
    def get_date(self):
        return humanize.naturaltime(self.updated_at)    

class Shipping(models.Model):
   
    user = models.ForeignKey(CustomUser,related_name="shipping",on_delete=models.CASCADE,null=True)
    order = models.OneToOneField(Order,related_name="shipping",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=205,null=True)
    phone = models.CharField(max_length=205,null=True)
    email = models.CharField(max_length=205,null=True)

    company_name = models.CharField(max_length=205,null=True)
    address_1 = models.CharField(max_length=205,null=True)
    address_2 = models.CharField(max_length=205,null=True)
    city = models.CharField(max_length=205,null=True)
    postcode = models.CharField(max_length=205,null=True)
    state = models.CharField(max_length=205,null=True)

    shpping_address = models.CharField(max_length=2055,null=True)


class GlobalSettings(models.Model):
    site_name = models.CharField(max_length=255)
    site_name_nepali = models.CharField(max_length=255,null=True)
    site_email = models.EmailField()
    configure_email = models.EmailField(null=True)
    site_contact = models.CharField(max_length=255,null=True)
    site_contact_nepali = models.BigIntegerField(null=True)
    site_address = models.CharField(max_length=255)
    site_address_nepali = models.CharField(max_length=255,null=True)
    fb_link = models.CharField(max_length=255,null=True)
    twitter_link = models.CharField(max_length=255,null=True)
    linkedin_link = models.CharField(max_length=255,null=True)
    tiktok_link = models.CharField(max_length=255,null=True) 
    other_link = models.CharField(max_length=255,null=True) #youtube
    page_title = models.CharField(max_length=255)
    page_keyword = models.CharField(max_length=200,null=True)
    page_discription = models.TextField(max_length=5000,null=True)
    image1 = models.ImageField(upload_to='global/fav_ico', null=True)
    image2 = models.ImageField(upload_to='global/logo', null=True)
    image3 = models.ImageField(upload_to='global/footer_logo', null=True)
    Image4 = models.ImageField(upload_to='ads/', null=True) #1
    Image5 = models.ImageField(upload_to='ads/', null=True) #2
    Image6 = models.ImageField(upload_to='ads/', null=True) #3
    Image7 = models.ImageField(upload_to='ads/', null=True) #4
    Image8 = models.ImageField(upload_to='ads/', null=True) #5
    Image9 = models.ImageField(upload_to='ads/', null=True) #6
    Image10 = models.ImageField(upload_to='ads/', null=True) #7
    Image11 = models.ImageField(upload_to='ads/', null=True) #8
    Image12 = models.ImageField(upload_to='ads/', null=True) #9
    Image13 = models.ImageField(upload_to='ads/', null=True) #10
    created_at = models.DateTimeField(auto_now=True,null=True) 
    updated_at = models.DateTimeField(auto_now=True,null=True) 

    def __str__(self):
        return "{name:"+self.name+","+"global_setting"+str(self.id)+"}"

class Team(models.Model):
    name = models.CharField(max_length=255)
    post = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, null=True)
    long_contents = models.TextField(max_length=255,null=True)
    profile_picture = models.ImageField(upload_to='founders/', null=True)

class Blog(models.Model):
    title = models.CharField(max_length=2000,null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    main_title = models.TextField(max_length=5000,null=True)
    discription = models.TextField(max_length=5000,null=True)
    author = models.CharField(max_length=255,null=True)
    banner_image = models.ImageField(upload_to='blogs/banner', null=True)
    icon_image = models.ImageField(upload_to='blogs/icon', null=True)
    status = models.BooleanField(default=True)
    def get_date(self):
        return humanize.naturaltime(self.updated_at)

# class Wishlist(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,null=True)
#     product = models.ForeignKey('Products',on_delete=models.CASCADE)
#     ishere = models.SmallIntegerField(default=True)   # ishere field 1 =>wishlist |||| 0 => cart ||| 2=> order
#     color = models.CharField(max_length=50, null=True)
#     size = models.CharField(max_length=50, null=True)
#     quantity = models.IntegerField(null=True,default=1)
#     temp_id = models.BigIntegerField(null=True)

# class Review(models.Model):
#     product = models.ForeignKey('Products',related_name="review",on_delete=models.CASCADE) 
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,null=True)
#     str_choice = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)]
#     star = models.CharField(max_length=50,choices=str_choice,default=0)
#     created_at = models.DateTimeField(auto_now=True,null=True) 
#     updated_at = models.DateTimeField(auto_now=True,null=True) 

class ContactUs(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)
    read_unread = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def get_date(self):
        return humanize.naturaltime(self.updated_at)
    
class ShippingAddress(models.Model):
    country = models.CharField(max_length=255 , null=True)
    district = models.CharField(max_length=255 , null=True)
    state = models.CharField(max_length=255 , null=True)
    city = models.CharField(max_length=255 , null=True)
    company_name = models.CharField(max_length=255 , null=True)
    mobile_number = models.CharField(max_length=255 , null=True)




