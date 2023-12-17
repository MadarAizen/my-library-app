# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User





class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    nameofbook = models.CharField(db_column='nameOfBook', max_length=25, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(max_length=13, blank=True, null=True)
    genre = models.CharField(max_length=10, blank=True, null=True)
    collateralprice = models.IntegerField(db_column='collateralPrice', blank=True, null=True)  # Field name made lowercase.
    rentalprice = models.IntegerField(db_column='rentalPrice', blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return str(self.book_id)+' '+self.nameofbook+' '+self.author+' '+str(self.collateralprice)+' '+str(self.rentalprice)
    class Meta:
        managed = False
        db_table = 'books'


class Fines(models.Model):
    fine_id = models.IntegerField(primary_key=True)
    appeal_id = models.IntegerField(blank=True, null=True)
    fineprice = models.IntegerField(db_column='finePrice', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fines'


# class Readers(models.Model):
#     reader_id = models.IntegerField(primary_key=True)
#     surname = models.CharField(max_length=15, blank=True, null=True)
#     name = models.CharField(max_length=15, blank=True, null=True)
#     fathersname = models.CharField(db_column='fathersName', max_length=15, blank=True, null=True)  # Field name made lowercase.
#     address = models.CharField(max_length=30, blank=True, null=True)
#     phonenumber = models.CharField(db_column='phoneNumber', max_length=25, blank=True, null=True)  # Field name made lowercase.
#     def __str__(self):
#         return str(self.reader_id)+' '+self.surname+' '+self.name
#     class Meta:
#         managed = False
#         db_table = 'readers'



class Product(models.Model):
    product_name = models.CharField(max_length=25, blank=True,
                              null=True)  # Field name made lowercase.
    product_price = models.IntegerField(blank=True, null=True)



class Appeals(models.Model):
    appeal_id = models.IntegerField(primary_key=True)
    #reader_id = models.IntegerField(blank=True, null=True)
    #book_id = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    issuedate = models.DateField(db_column='issueDate')  # Field name made lowercase.
    dateofreturn = models.DateField(db_column='dateOfReturn', blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return str(self.appeal_id)+" "+str(self.book.nameofbook)+" "+str(self.reader.username)+' '+str(self.issuedate)+" "+str(self.dateofreturn)

    class Meta:
        managed = False
        db_table = 'appeals'

class Sales(models.Model):
    sale_id = models.IntegerField(primary_key=True)
    reader_id = models.IntegerField(blank=True, null=True)
    percentofsale = models.IntegerField(db_column='percentOfSale', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sales'


class Testik(models.Model):
    dateofreturn = models.DateField(db_column='dateOfReturn', blank=True, null=True)  # Field name made lowercase.
    appeal_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'testik'
