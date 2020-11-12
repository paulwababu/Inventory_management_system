from django.db import models

# Create your models here.

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    price = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to =  models.CharField(max_length=50, blank=True, null=True)
    phone_number =  models.CharField(max_length=50, blank=True, null=True)
    created_by =  models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name + ' ' + str(self.quantity) + ' ' + str(self.price)

class StockHistory(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)        

class Transaction(models.Model):
    employee_name = models.CharField(max_length=50, blank=False)
    transaction_amount = models.IntegerField(default='0', blank=False)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)        
    product_ids = models.CharField(max_length=256)
    items_count = models.CharField(max_length=256)

class Order(models.Model):
    id= models.OneToOneField('stock', on_delete=models.PROTECT, primary_key=True, unique=True)
    employee_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)

class OrderQuantity(models.Model):
    quantity = models.IntegerField(default='0', blank=True, null=True)
