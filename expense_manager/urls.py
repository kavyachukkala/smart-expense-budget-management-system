from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from expenses.views import (
    register,
    dashboard,
    add_category,
    add_expense,
    add_income,
    set_budget,
    transaction_history,
    edit_expense,
    delete_expense
)


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path(
        "register/",
        register,
        name="register"
    ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="expenses/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="login"
        ),
        name="logout"
    ),

    path(
        "add-category/",
        add_category,
        name="add_category"
    ),

    path(
        "add-expense/",
        add_expense,
        name="add_expense"
    ),

    path(
        "add-income/",
        add_income,
        name="add_income"
    ),

    path(
        "set-budget/",
        set_budget,
        name="set_budget"
    ),

    # Step 8 - Transaction History

    path(
        "transactions/",
        transaction_history,
        name="transaction_history"
    ),

    path(
        "edit-expense/<int:expense_id>/",
        edit_expense,
        name="edit_expense"
    ),

    path(
        "delete-expense/<int:expense_id>/",
        delete_expense,
        name="delete_expense"
    ),
]
