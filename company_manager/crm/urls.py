from django.urls import path
import crm.views as views
# importuju pohledy, . ze sameho adresare, nebo lze brat jako root adresar

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), # django umi psat pohledy jako funkce i jako tridy
    path('company/create', views.CompanyCreateView.as_view(), name='company_create'),
    path("companies", views.CompanyListView.as_view(), name="companies"),
    path("opportunity/create_opportunity", views.OpportunityCreateView.as_view(), name="opportunity_create"),
    path("opportunity/update/<int:pk>", views.OpportunityUpdateView.as_view(), name="opportunity_update"),
    path("employee/", views.EmployeeUpdateView.as_view(), name="employee_update")

]
