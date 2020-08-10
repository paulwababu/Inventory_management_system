from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv
from .models import *
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date
from django.db.models import Sum
import json
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    title = 'welcome to our homepage'
    form = "welcome"
    context = {
        "title": title,
        "form": form,
    }
    return render(request, "home.html", context)

@login_required
def list_items(request):
    header = 'LIST OF ITEMS'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
	    queryset = Stock.objects.filter(category__icontains=form['category'].value(),
								   item_name__icontains=form['item_name'].value()
									)
                                    
	    context = {
	    "form": form,
	    "header": header,
	    "queryset": queryset,
}
    return render(request, "list_items.html", context)

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)    

@login_required
def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save(), messages.success(request, 'Successfully Updated')
			return redirect('/list_items')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)
    
@login_required	
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/list_items')
    return render(request, 'delete_items.html')        

def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)


@login_required
@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)

    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(
            request,
            "Issued SUCCESSFULLY. "
            + str(instance.quantity)
            + " "
            + str(instance.item_name)
            + "s now left in Store",
        )
        instance.save()
        sell_transaction = Transaction(
            employee_name= request.user.username,
            transaction_type= "selling",
            transaction_amount= instance.price * instance.issue_quantity,
            timestamp= date.today(),
            item_name= instance.item_name,
        )
        sell_transaction.save()
        return redirect("/stock_detail/" + str(instance.id))
    context = {
        "title": "Issue " + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": "Issue By: " + str(request.user),
	}
    return render(request, "add_items.html", context)



@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(
            request,
            "Received SUCCESSFULLY. "
            + str(instance.quantity)
            + " "
            + str(instance.item_name)
            + "s now in Store",
        )

        return redirect("/stock_detail/" + str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": "Reaceive " + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": "Receive By: " + str(request.user),
    }
    return render(request, "add_items.html", context)

@login_required
def list_history(request):
	header = 'LIST OF ITEMS'
	queryset = StockHistory.objects.all()
	context = {
		"header": header,
		"queryset": queryset,
	}
	return render(request, "list_history.html",context)

@login_required
def report(request):
    data =Transaction.objects.values('item_name').annotate(Sum('transaction_amount'))
    categories = [items["item_name"] for items in data]
    user_count = User.objects.all().count()
    prices = [items["transaction_amount__sum"] for items in data]
    total_sales = sum(prices)
    print(data, categories, prices)
    return render(request, "report-1.html", {'categories':json.dumps(categories), 'prices':json.dumps(prices), 'user_count':json.dumps(user_count),'total_sales':json.dumps(total_sales) })
