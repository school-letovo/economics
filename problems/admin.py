from django.contrib import admin

# Register your models here.

from .models import Problem, Assignment

admin.site.register(Problem)

class AssignmentAdmin(admin.ModelAdmin):
    fields = ['person', 'problem', 'date_deadline']
    def save_model(self, request, obj, form, change):
        obj.assigned_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.readonly_fields = ['date_assigned', 'assigned_by']
            self.fields = ['person', 'problem', 'date_deadline', 'assigned_by', 'date_assigned']
        else:
            self.readonly_fields = []
            self.fields = ['person', 'problem', 'date_deadline']
        form = super().get_form(request, obj, **kwargs)
        return form

admin.site.register(Assignment, AssignmentAdmin)
