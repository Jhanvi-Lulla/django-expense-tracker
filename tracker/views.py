from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ItemFormModel
from .models import expense


def _my_expenses(request):
    """Only the logged-in user's own expenses.
    Every view below uses this, so one user can never see,
    edit or delete another user's data."""
    return expense.objects.filter(user=request.user)


def _default_image():
    return expense._meta.get_field("Image").default


# ------------------------ welcome (public page) ------------------------
def welcome(request):
    return render(request, "tracker/welcome.html")


# ------------------------ list ------------------------
@login_required
def index(request):
    expense_list = _my_expenses(request).order_by("-id")

    query = request.GET.get("search", "").strip()
    if query:
        expense_list = expense_list.filter(Expense_reason__icontains=query)

    total = expense_list.aggregate(total=Sum("Amount"))["total"] or 0
    return render(request, "tracker/index2.html", {
        "expense_list": expense_list,
        "total_sum": total,
        "query": query,
    })


# ------------------------ detail ------------------------
@login_required
def detail(request, expense_id):
    obj = get_object_or_404(_my_expenses(request), pk=expense_id)
    return render(request, "tracker/detail.html", {"obj": obj})


# ------------------------ add ------------------------
@login_required
def add_item(request):
    form = ItemFormModel(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user  # <-- the important line: item belongs to this user
        if not obj.Image:
            obj.Image = _default_image()
        obj.save()
        messages.success(request, "Expense added.")
        return redirect("index")
    return render(request, "tracker/addItem.html", {"form": form, "title": "Add expense"})


# ------------------------ update ------------------------
@login_required
def update_item(request, expense_id):
    item = get_object_or_404(_my_expenses(request), pk=expense_id)
    form = ItemFormModel(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        if not obj.Image:
            obj.Image = _default_image()
        obj.save()
        messages.success(request, "Expense updated.")
        return redirect("index")
    return render(request, "tracker/addItem.html", {"form": form, "title": "Update expense"})


# ------------------------ delete ------------------------
@login_required
def delete_item(request, expense_id):
    obj = get_object_or_404(_my_expenses(request), pk=expense_id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Expense deleted.")
        return redirect("index")
    return render(request, "tracker/delete_item.html", {"obj": obj})


# ------------------------ total ------------------------
@login_required
def pdf(request):
    total = _my_expenses(request).aggregate(total=Sum("Amount"))["total"] or 0
    return render(request, "tracker/pdf.html", {
        "total_sum": total,
        "username": request.user.username,
    })
