from django.views.generic import CreateView, ListView, TemplateView, UpdateView
import crm.models as models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from crm.forms import CompanyForm


from django.utils.translation import gettext as _

class IndexView(TemplateView):
    template_name = "index.html"


class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    template_name = "company/create_company.html"
    success_url = reverse_lazy("index")
    # presmerovani po uspesnem vytvoreni
    form_class = CompanyForm
    success_message = "Company was created successfully"


class CompanyListView(LoginRequiredMixin, ListView):
    model = models.Company
    template_name = "company_list.html"


class OpportunityCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'crm.add_opportunity'
    model = models.Opportunity
    template_name = "opportunity/create_opportunity.html"
    fields = ["company", "sales_manager", "primary_contact", "description", "status"]
    success_url = reverse_lazy("index")
    # Translators: This message is shown after successfully created
    success_message = _("company created!")

class OpportunityUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'crm.change_opportunity'
    model = models.Opportunity
    template_name = "opportunity/update_opportunity.html"
    fields = ["company", "sales_manager", "primary_contact", "description",
              "status"]
    success_url = reverse_lazy("index")


class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = ["department", "phone_number", "office_number", "manager"]
    template_name = "employee/update_employee.html"
    success_url = reverse_lazy("index")
    success_message = "Data was updated successfully"

    def get_object(self, queryset=None):
        return self.request.user.employee