from django.urls import path
from . import views

urlpatterns = [
    path("", views.role_landing, name="role-landing"),
    path("dashboard/", views.employee_dashboard, name="employee-dashboard"),
    path("accepted/", views.accepted_cases, name="accepted-cases"),
    path("service-areas/", views.service_areas, name="service-areas"),
    path("case-payouts/", views.case_payouts, name="case-payouts"),
    path("employees/register/", views.register_employee, name="register-employee"),
    path("employees/<str:employee_id>/profile/", views.employee_profile, name="employee-profile"),
    path("profile/", views.profile_lookup, name="profile-lookup"),
    path("auth/", views.employee_auth, name="employee-auth"),
    path("official/login/", views.official_login, name="official-login"),
    path("official/dashboard/", views.official_dashboard, name="official-dashboard"),
    path("official/post-case/", views.post_case, name="post-case"),
    path("official/employees/", views.official_employees, name="official-employees"),
    path("logout/", views.employee_logout, name="employee-logout"),
    path("cases/<int:case_id>/<str:decision>/", views.respond_to_case, name="respond-to-case"),
]
