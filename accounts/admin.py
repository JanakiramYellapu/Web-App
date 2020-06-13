from django.contrib import admin
from .models import Date, User, AccountInfo, Transaction, Expense

# Register your models here.

admin.site.register(Date)
admin.site.register(User)
admin.site.register(AccountInfo)
admin.site.register(Transaction)
admin.site.register(Expense)
