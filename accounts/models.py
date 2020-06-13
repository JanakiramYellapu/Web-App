from django.db import models
import datetime

# Create your models here.


class Date(models.Model):
    date = models.DateField(unique = True)

    def __str__(self):
        return f"{self.date}"


class User(models.Model):
    firstName = models.CharField(max_length = 60)
    lastName = models.CharField(max_length =30, blank = True, null = True)
    mobileNo = models.CharField(max_length = 10, blank = True, null = True)
    dates = models.ManyToManyField(Date, through = 'Transaction',
                        through_fields = ('userId','dateId'),
                        related_name="users")

    def __str__(self):
        return f"  {self.firstName} {self.lastName}  "

class Transaction(models.Model):
    userId = models.ForeignKey(User, on_delete = models.CASCADE)
    dateId = models.ForeignKey(Date, on_delete = models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.userId} {self.dateId} {self.amount}"


class AccountInfo(models.Model):
    userId = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.FloatField(default = 0)
    openDate = models.DateField(default=datetime.date.today)
    closeDate = models.DateField(default = datetime.date.today() + datetime.timedelta(days =90))
    closedDate = models.DateField(blank = True, null = True)
    status = models.CharField(max_length = 15, default ="open")

    def __str__(self):
        return f"{self.id} : {self.userId} {self.openDate} {self.closeDate} {self.closedDate} {self.status}"


class Expense(models.Model):
    item = models.CharField(max_length=70)
    amount = models.IntegerField()
    dateId = models.ForeignKey(Date, on_delete = models.CASCADE)

    def __str__(self):
        return f" {self.dateId} {self.item} {self.amount}"
