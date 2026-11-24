from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
import json
import re
import json
from pathlib import Path
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CollectionRequest

def add_demo_cases():
    if CollectionRequest.objects.exists():
        return
    CollectionRequest.objects.bulk_create([
        CollectionRequest(case_number="PD-301", customer_name="Priya Sharma", collection_type="Routine blood work", address="Sector 62, Noida", pin_code="201309", payout_amount=150),
        CollectionRequest(case_number="PD-302", customer_name="Mohit Kumar", collection_type="Fasting sample", address="Indirapuram, Ghaziabad", pin_code="201014", payout_amount=180),
    ])

def role_landing(request):
    return render(request, "employees/role_landing.html")

@login_required(login_url="/auth/")
def employee_dashboard(request):
    add_demo_cases()
    cases = CollectionRequest.objects.filter(status=CollectionRequest.Status.OPEN).order_by("-created_at")
    accepted_cases = CollectionRequest.objects.filter(status=CollectionRequest.Status.ACCEPTED).order_by("-created_at")
    total_payout = accepted_cases.aggregate(total=Sum("payout_amount"))["total"] or 0
    return render(request, "employees/dashboard.html", {"cases": cases, "accepted_cases": accepted_cases, "total_payout": total_payout})

def employee_auth(request):
    error = ""
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "register":
            username, password, name, phone, email, pin_code = request.POST.get("username", "").strip(), request.POST.get("password", ""), request.POST.get("full_name", "").strip(), request.POST.get("phone", "").strip(), request.POST.get("email", "").strip(), request.POST.get("pin_code", "").strip()
            if not username or not password or not name or not phone or not email or not pin_code:
                error = "Complete all registration fields."
            elif not pin_code.isdigit() or len(pin_code) != 6:
                error = "Enter a valid 6-digit employee PIN code."
            elif len(password) < 6 or len(password) > 8 or not re.fullmatch(r"(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d]).{6,8}", password):
                error = "Password must be 6-8 characters and include letters, numbers, and one special character."
            elif User.objects.filter(username=username).exists():
                error = "That username is already registered."
            else:
                user = User.objects.create_user(username=username, password=password, first_name=name, email=email)
                employee = Employee.objects.create(user=user, full_name=name, phone=phone, pin_code=pin_code, email=email, availability=Employee.Availability.OFFLINE)
                return render(request, "employees/registered.html", {"employee": employee})
        elif action == "login":
            login_value = request.POST.get("username", "").strip()
            password = request.POST.get("password", "")
            user = authenticate(request, username=login_value, password=password)
            if user is None:
                employee = Employee.objects.filter(employee_id__iexact=login_value).select_related("user").first()
                if employee and employee.user:
                    user = authenticate(request, username=employee.user.username, password=password)
            if user and hasattr(user, "employee_profile"):
                employee = user.employee_profile
                if not (employee.email_verified and employee.phone_verified):
                    error = "Your email and phone must both be verified before dashboard access."
                else:
                    login(request, user)
                    return redirect("employee-dashboard")
            error = "Invalid employee username or password."
    return render(request, "employees/auth_v3.html", {"error": error})

def employee_logout(request):
    logout(request)
    return redirect("employee-auth")

def official_login(request):
    error = ""
    if request.method == "POST":
        if request.POST.get("secret_code", "") == settings.OFFICIAL_SECRET_CODE:
            request.session["official_access"] = True
            return redirect("official-dashboard")
        error = "Invalid official secret code."
    return render(request, "employees/official_login_v2.html", {"error": error})

def official_dashboard(request):
    if not request.session.get("official_access"):
        return redirect("official-login")
    return render(request, "employees/official_dashboard_v4.html", {"employees": Employee.objects.all().order_by("full_name"), "open_cases": CollectionRequest.objects.filter(status=CollectionRequest.Status.OPEN), "accepted_cases": CollectionRequest.objects.filter(status=CollectionRequest.Status.ACCEPTED).select_related("accepted_by")})

def post_case(request):
    if not request.session.get("official_access"):
        return redirect("official-login")
    message = ""
    if request.method == "POST":
        last = CollectionRequest.objects.order_by("-id").first()
        next_number = (last.id + 301) if last else 301
        CollectionRequest.objects.create(case_number=f"PD-{next_number}", customer_name=request.POST.get("customer_name", "").strip(), collection_type=request.POST.get("collection_type", "Routine blood work"), address=request.POST.get("address", "").strip(), pin_code=request.POST.get("pin_code", "").strip(), payout_amount=request.POST.get("payout_amount", "0"))
        message = "Customer collection posted for employees."
    return render(request, "employees/post_case.html", {"message": message})

def official_employees(request):
    if not request.session.get("official_access"):
        return redirect("official-login")
    employees = Employee.objects.all().prefetch_related("accepted_collections").order_by("full_name")
    return render(request, "employees/official_employees.html", {"employees": employees})

def accepted_cases(request):
    rows = CollectionRequest.objects.filter(status=CollectionRequest.Status.ACCEPTED).order_by("-created_at")
    now = timezone.localtime()
    monthly_rows = rows.filter(created_at__year=now.year, created_at__month=now.month)
    daily_rows = monthly_rows.filter(created_at__date=now.date())
    return JsonResponse({"total": sum((row.payout_amount for row in rows), 0), "daily": sum((row.payout_amount for row in daily_rows), 0), "monthly": sum((row.payout_amount for row in monthly_rows), 0), "count": rows.count(), "items": [{"case": row.case_number, "customer": row.customer_name, "type": row.collection_type, "payout": str(row.payout_amount)} for row in rows]})

def service_areas(request):
    data = json.loads((Path(__file__).resolve().parent / "service_areas.json").read_text(encoding="utf-8"))
    return JsonResponse({"areas": data, "count": len(data)})

def case_payouts(request):
    rows = CollectionRequest.objects.filter(status=CollectionRequest.Status.OPEN)
    return JsonResponse({str(row.pk): str(row.payout_amount) for row in rows})

@csrf_exempt
def register_employee(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required."}, status=405)
    try:
        payload = json.loads(request.body)
        employee = Employee.objects.create(full_name=payload["full_name"], phone=payload["phone"], email=payload.get("email", ""), availability=payload.get("availability", Employee.Availability.OFFLINE), latitude=payload.get("latitude"), longitude=payload.get("longitude"))
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        return JsonResponse({"error": f"Invalid employee data: {exc}"}, status=400)
    return JsonResponse({"id": employee.id, "employee_id": employee.employee_id, "message": "Employee stored successfully."}, status=201)

def employee_profile(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    if request.method == "POST":
        employee.full_name = request.POST.get("full_name", employee.full_name)
        employee.phone = request.POST.get("phone", employee.phone)
        employee.pin_code = request.POST.get("pin_code", employee.pin_code)
        employee.email = request.POST.get("email", employee.email)
        if request.FILES.get("profile_picture"):
            employee.profile_picture = request.FILES["profile_picture"]
        employee.save()
    return render(request, "employees/profile.html", {"employee": employee})

def profile_lookup(request):
    return render(request, "employees/profile_lookup.html")

@require_POST
def respond_to_case(request, case_id, decision):
    if decision not in (CollectionRequest.Status.ACCEPTED, CollectionRequest.Status.REJECTED):
        return JsonResponse({"error": "Invalid decision."}, status=400)
    case = get_object_or_404(CollectionRequest, pk=case_id, status=CollectionRequest.Status.OPEN)
    case.status = decision
    if decision == CollectionRequest.Status.ACCEPTED and hasattr(request.user, "employee_profile"):
        case.accepted_by = request.user.employee_profile
    case.save(update_fields=["status", "accepted_by"])
    return JsonResponse({"case_id": case.pk, "status": case.get_status_display()})
