from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Category, Income, Expense, Budget


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("dashboard")

    else:
        form = UserCreationForm()

    return render(
        request,
        "expenses/register.html",
        {"form": form}
    )


@login_required
def dashboard(request):

    total_income = Income.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expenses = Expense.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    balance = total_income - total_expenses

    budget = Budget.objects.filter(
        user=request.user
    ).order_by("-id").first()

    if budget:
        budget_amount = budget.amount
    else:
        budget_amount = 0

    remaining_budget = budget_amount - total_expenses

    recent_expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")[:5]

    # Expense data grouped by category

    category_data = Expense.objects.filter(
        user=request.user
    ).values(
        "category__name"
    ).annotate(
        total=Sum("amount")
    ).order_by("-total")

    category_names = []
    category_amounts = []

    for item in category_data:

        category_names.append(
            item["category__name"]
        )

        category_amounts.append(
            float(item["total"])
        )

    context = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "budget_amount": budget_amount,
        "remaining_budget": remaining_budget,
        "recent_expenses": recent_expenses,

        "category_names": category_names,
        "category_amounts": category_amounts,
    }

    return render(
        request,
        "expenses/dashboard.html",
        context
    )
@login_required
def add_category(request):

    if request.method == "POST":

        category_name = request.POST.get("name")

        if category_name:
            Category.objects.create(
                name=category_name,
                user=request.user
            )

            messages.success(
                request,
                "Category added successfully!"
            )

            return redirect("add_expense")

    return render(
        request,
        "expenses/add_category.html"
    )


@login_required
def add_expense(request):

    categories = Category.objects.filter(
        user=request.user
    )

    if request.method == "POST":

        title = request.POST.get("title")
        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        description = request.POST.get("description")

        category = get_object_or_404(
            Category,
            id=category_id,
            user=request.user
        )

        Expense.objects.create(
            user=request.user,
            title=title,
            category=category,
            amount=amount,
            date=date,
            description=description
        )

        messages.success(
            request,
            "Expense added successfully!"
        )

        return redirect("dashboard")

    return render(
        request,
        "expenses/add_expense.html",
        {"categories": categories}
    )
@login_required
def add_income(request):

    if request.method == "POST":

        source = request.POST.get("source")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        Income.objects.create(
            user=request.user,
            source=source,
            amount=amount,
            date=date
        )

        messages.success(
            request,
            "Income added successfully!"
        )

        return redirect("dashboard")

    return render(
        request,
        "expenses/add_income.html"
    )
@login_required
def set_budget(request):

    if request.method == "POST":

        month = request.POST.get("month")
        amount = request.POST.get("amount")

        Budget.objects.update_or_create(
            user=request.user,
            month=month,
            defaults={
                "amount": amount
            }
        )

        messages.success(
            request,
            "Budget set successfully!"
        )

        return redirect("dashboard")

    return render(
        request,
        "expenses/set_budget.html"
    )
@login_required
def transaction_history(request):

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "expenses/transaction_history.html",
        {
            "expenses": expenses
        }
    )


@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    categories = Category.objects.filter(
        user=request.user
    )

    if request.method == "POST":

        expense.title = request.POST.get("title")
        expense.amount = request.POST.get("amount")
        expense.date = request.POST.get("date")
        expense.description = request.POST.get("description")

        category_id = request.POST.get("category")

        expense.category = get_object_or_404(
            Category,
            id=category_id,
            user=request.user
        )

        expense.save()

        messages.success(
            request,
            "Expense updated successfully!"
        )

        return redirect("transaction_history")

    return render(
        request,
        "expenses/edit_expense.html",
        {
            "expense": expense,
            "categories": categories
        }
    )


@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":

        expense.delete()

        messages.success(
            request,
            "Expense deleted successfully!"
        )

        return redirect("transaction_history")

    return render(
        request,
        "expenses/delete_expense.html",
        {
            "expense": expense
        }
    )
