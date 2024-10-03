from django.shortcuts import render,redirect

from budget.forms import ExpenseForm

from django.views.generic import View

from django.contrib import messages

from budget.models import Expense

from django.db.models import Q

from django.db.models import Count,Sum



class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"expense_create.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

           form_instance.save()

           messages.success(request,"expense added successfully")


           return redirect("expense_add")

        else:

            messages.error(request,"error in adding")


            return render(request,"expense_create.html",{"form":form_instance})




class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        
        selected_category=request.GET.get("category","all")


        search_text=request.GET.get("search_text")

       
           
        if selected_category=="all":

             qs=Expense.objects.all()
            
        else:

            qs=Expense.objects.filter(category=selected_category)

        

        if search_text!=None:

            qs=Expense.objects.filter(Q(title__icontains=search_text)|Q(user__icontains=search_text))



        return render(request,"expense_list.html",{"expenses":qs})






class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_obj)

        return render(request,"expense_update.html",{"form":form_instance})

    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            Expense.objects.filter(id=id).update(**data)

            messages.success(request,"Table updated successfully")

            return redirect("expense_list")
        
        else:
            messages.error(request,"Updation Failed")
            return render(request,"expense_update.html",{"form":form_instance})



class ExpenseDeleteView(View):

            def get(self,request,*args,**kwargs):

                id=kwargs.get("pk")

                Expense.objects.get(id=id).delete()

                messages.success(request,"Data deleted successfully")

                return redirect("expense_list")




class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):


       qs=Expense.objects.all()

       total_expense_count=qs.count()

       category_summary=Expense.objects.all().values("category").annotate(exp_count=Count("category"))

       total_expense=Expense.objects.all().values("amount").aggregate(exp_sum=(Sum("amount")))

       category_total=Expense.objects.all().values("category").annotate(cat_total=(Sum("amount")))

       print(category_total)
                
       context={

        "total_expense_count":total_expense_count,

        "category_summary":category_summary,

        "total_expense":total_expense,

        "category_total":category_total
       }

       return render(request,"expense_summary.html",context)


    