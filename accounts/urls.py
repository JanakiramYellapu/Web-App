from django.urls import path

from . import views

urlpatterns =[
    path("" , views.index, name = "index"),
    path("sheetEntry" , views.sheetEntry, name = "sheetEntry"),
    path("sheetEntry/form" , views.selectDate, name = "selectDate"),
    path("sheetEntry/form/data" , views.sheetData, name = "sheetData"),
    path("user" , views.user, name = "user"),
    path("user/statement" , views.statement, name = "statement"),
    path("user/statement/getInfo" , views.getInfo, name = "getInfo"),
    path("user/deleteUser" , views.deleteUser, name = "deleteUser"),
    path("user/deleteUser/form" , views.deleteUserForm, name = "deleteUserForm"),
    path("user/newAccount" , views.newAccount, name = "newAccount"),
    path("user/newAccount/existingUserAccountForm" , views.existing, name = "existing"),
    path("user/newAccount/new" , views.new, name = "new"),
    path("user/newAccount/new/form" , views.newAccountInfoEntry, name = "newAccountInfoEntry"),
    path("user/newAccount/existing/form" , views.accountInfoEntry, name = "accountInfoEntry"),
    path("user/closeAccount" , views.closeAccount, name = "closeAccount"),
    path("user/closeAccount/form" , views.closeAccountForm, name = "closeAccountForm"),
    path("sheetEntry/form/expense" , views.expenseAmount, name = "expenseAmount"),
    path("expenseDate/expenses" , views.expense, name = "expense"),
    path("expenseDate" , views.expenseDate, name = "expenseDate"),

]
