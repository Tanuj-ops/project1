from django.db import models
from django.contrib.auth.models import User

class category(models.Model):
    cat_name = models.CharField(max_length=100)
    cover_image = models.FileField(upload_to='category_images/')
    description = models.TextField()

    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name

class register_table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    profile_image = models.FileField(upload_to='profile_images/', null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    age = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    upi_number = models.CharField(max_length=20, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username
    
class add_product(models.Model):
    product_category = models.ForeignKey(category, on_delete=models.CASCADE)
    Artist = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_image = models.FileField(upload_to='product_images/')
    description = models.TextField()
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
class cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(add_product,on_delete = models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username
    
class order(models.Model):
    cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=250)
    product_ids = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username
    
class feature_product(models.Model):
    name = models.ForeignKey(add_product, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.name.product_name