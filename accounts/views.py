from django.shortcuts import render
# from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Date, Transaction, AccountInfo, Expense
import datetime
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

# Create your views here.
def index(request):
    return render(request, "accounts/index.html")

def sheetEntry(request):
    return render(request, "accounts/selectDate.html")


def user(request):
    return render(request, "accounts/user.html")

 #  /users/
def statement(request):
    context ={
        "users" : User.objects.all()
    }
    return render(request, "accounts/selectuser.html", context)

#  /users/
def newAccount(request):
    return render(request, "accounts/existingOrNot.html")

#  /users/
def deleteUser(request):
    context ={
        "users" : User.objects.all()
    }
    return render(request, "accounts/deleteUserForm.html", context)

# users/statement/
def getInfo(request):
    try :
        userId = int(request.POST["userObj"])
        user = User.objects.get(pk = userId)
        userData = Transaction.objects.filter(userId = user)
    except KeyError:
        return render(request, "accounts/error.html", {"message" : "Please Enter"})
    except Transaction.DoesNotExist:
        return render(request, "accounts/error.html", {"message" : "No transactions"})
    except User.DoesNotExist:
        return render(request, "accounts/error.html", {"message" : "Invalid User"})
    total = userData.aggregate(Sum('amount'))
    a = AccountInfo.objects.filter(userId =user, status ="open")
    context ={
        "userData" : userData,
        "user"     : user,
        "total"    : total,
        "accountInfo" : a
     }
    return render(request, "accounts/getInfo.html", context)


#  users/newAccount
def existing(request):
    context ={
        "users" : User.objects.all()
    }
    return render(request, "accounts/existingUserAccountForm.html", context)

#  users/newAccount
def new(request):
    return render(request, "accounts/newAccountOpenForm.html")

@csrf_exempt
def accountInfoEntry(request):
    try :
        userId = request.POST["userObj"]
        type =  request.POST['type']
        amount = request.POST["amount"]
        date = request.POST['date']
        user = User.objects.get(pk = userId)
    except KeyError:
        return render(request, "accounts/error.html", {"message" : "Enter Again"})
    except User.DoesNotExist:
        return render(request, "accounts/error.html", {"message" : "Invalid User"})
    d = Date.objects.filter(date = date)
    if(not d.exists()):
        d = Date(date=date)
        d.save()
    d = Date.objects.get(date = date)
    message ={
        "status" : "open",
        "firstName" : user.firstName,
        "date" : d.date
    }
    if(type == "single"):
        try:
            a = AccountInfo.objects.filter(userId = user, status="open")
        except AccountInfo.DoesNotExist:
            a = AccountInfo(userId = user, openDate =date, amount = amount)
            a.save()
            message["status"] = "closed"

    elif(type == "multiple") :
        a = AccountInfo(userId = user, openDate = date, amount = amount)
        a.save()
        message["status"] = "closed"
    return HttpResponse(
        json.dumps(message, cls=DjangoJSONEncoder),
        content_type = 'application/javascript; charset=utf8'
    )


@csrf_exempt
def newAccountInfoEntry(request):
    try:
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        mobileNo = request.POST["mobileNo"]
        amount = request.POST["amount"]
        date = request.POST['date']
    except KeyError:
        return render(request, "accounts/error.html", {"message" : "Please Enter"})
    u = User(firstName = firstName, lastName = lastName,
            mobileNo = mobileNo)
    u.save()
    d = Date.objects.filter(date = date)
    if(not d.exists()):
        d = Date(date=date)
        d.save()
    d = Date.objects.get(date = date)
    a = AccountInfo(userId = u, openDate = date,amount = amount)
    a.save()
    message = {
        "firstName" : u.firstName,
        "amount" : a.amount,
        "date" : d.date
    }
    return HttpResponse(
        json.dumps(message, cls=DjangoJSONEncoder),
        content_type = 'application/javascript; charset=utf8'
    )



# users/deleteUser
@csrf_exempt
def deleteUserForm(request):
    try:
        userId = int(request.POST["userObj"])
        user = User.objects.get(pk = userId)
    except User.DoesNotExist:
        return render(request, "accounts/error.html", {"message" : "Invalid user"})
    user.delete()
    return HttpResponse("Success!!!")

# closeAccount/
def closeAccount(request):
    context = {
        "users" : User.objects.all()
    }
    return render(request, 'accounts/selectUserClosingAccount.html', context)


@csrf_exempt
def closeAccountForm(request):
    userId = request.POST["userObj"]
    message = {"status" : "failed"}
    try:
        u = User.objects.get(pk=userId)
    except User.DoesNotExist:
        render(request, "accounts/error.html", {"message" : "Invalid user"})
    # close account
    a = AccountInfo.objects.get(userId = u, status="open")
    a.status = "closed"
    a.save()
    # Delete from transactions
    t = Transaction.objects.filter(userId = u)
    t.delete()
    message["status"] ="success"
    return HttpResponse(
        json.dumps(message, cls=DjangoJSONEncoder),
        content_type = 'application/javascript; charset=utf8'
    )



# sheetEntry/selectDate
def selectDate(request):
    date = request.POST["date"]
    # date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%d-%m-%Y")
    d = Date.objects.filter(date = date)
    if(not d.exists()):
        d = Date(date=date)
        d.save()
    d = Date.objects.get(date = date)
    context ={
        "date" : d,
        "users" : User.objects.all()
    }
    # return HttpResponse(d.id)
    return render(request, "accounts/sheetData.html", context)

@csrf_exempt
def sheetData(request):
    dateId = request.POST["date"]
    action = request.POST["action"]
    userId = int(request.POST["userId"])
    amount = request.POST["amount"]
    d = Date.objects.get(pk = dateId)
    if(action == "Save"):
        status ="updated"
        try:
            u = User.objects.get(pk = userId)
            t = Transaction.objects.get(userId =u, dateId =d)
        except User.DoesNotExist:
            return render(request, "accounts/error.html", {"message" : "Invalid user"})
        except Transaction.DoesNotExist:
            trst = Transaction(userId = u, dateId = d, amount = amount)
            trst.save()
            status = "saved"
        t = Transaction.objects.get(userId =u, dateId =d)
        prevAmount= t.amount
        t.amount = amount
        t.save()
        if(status == "saved"):
            message = {
                "status" : status,
                "user" : u.firstName,
                "date" : d.date,
                "amount" : amount,
            }
        elif (status == "updated"):
            message = {
                "status" : status,
                "user" : u.firstName,
                "date" : d.date,
                "amount" : amount,
                 "prevAmount" :prevAmount
            }
        # return JsonResponse(message)
        return HttpResponse(
            json.dumps(message, cls=DjangoJSONEncoder),
            content_type = 'application/javascript; charset=utf8'
        )
    elif (action == "Done"):
        # dummy variables
        exptot = 500
        finaltot = 0
        t = Transaction.objects.filter(dateId = d)
        total = t.aggregate(Sum('amount'));
        context ={
            "data" : t,
            "date" : d,
            "total" : total['amount__sum']
            }

        try:
            e = Expense.objects.filter(dateId = d)
        except Expense.DoesNotExist:
            exptot = 0
        if(not e.exists()):
             exptot = 0

        context['e'] = e
        if(exptot != 0):
            exptot = e.aggregate(Sum('amount'));
            context['exptot'] = exptot['amount__sum']
            finaltot = total['amount__sum'] - exptot['amount__sum']
        else:
            context['exptot'] = 0
            finaltot =  total['amount__sum']
        context['finaltot'] = finaltot

        return render(request, "accounts/finalSheet.html", context)

# /expense/
@csrf_exempt
def expenseAmount(request):
    dateId = request.POST['dateId']
    expense = request.POST['expense']
    amount = request.POST['amount']
    e = Expense.objects.filter(dateId = dateId, item = expense)
    d = Date.objects.get(pk = dateId)
    message ={
        "status" : "saved",
        "date" : d.date,
        "expense" : expense
    }
    if( not e.exists()) :
        e = Expense(dateId = d, amount = amount, item = expense)
        e.save()
    else:
        e = Expense.objects.get(dateId = dateId, item = expense)
        prevAmount = e.amount
        e.amount = amount
        e.save()
        message["status"] = "updated"
        message["prevAmount"] = prevAmount

    return HttpResponse(
        json.dumps(message, cls=DjangoJSONEncoder),
        content_type = 'application/javascript; charset=utf8'
    )
