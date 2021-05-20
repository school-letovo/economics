from django.contrib import admin

# Register your models here.

from .models import Problem, Assignment, Topic, Submit, Source, Variant, TestSet, TestSetAssignment, \
    TestSubmit, GroupTeacher, Paper, PaperAssignment, Theory, PaperObject
from .forms import SourceAdminForm

class AssignmentAdmin(admin.ModelAdmin):
    fields = ['person', 'problem', 'date_deadline', 'status']
    def save_model(self, request, obj, form, change):
        obj.assigned_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.readonly_fields = ['date_assigned', 'assigned_by', 'status']
            self.fields = ['person', 'problem', 'date_deadline', 'assigned_by', 'date_assigned', 'status']
        else:
            self.readonly_fields = []
            self.fields = ['person', 'problem', 'date_deadline']
        form = super().get_form(request, obj, **kwargs)
        return form

admin.site.register(Assignment, AssignmentAdmin)

class VariantInline(admin.TabularInline):
    model = Variant

class ProblemAdmin(admin.ModelAdmin):
    inlines = [VariantInline]

# class TaskOrderInline(admin.TabularInline):
#     model = TaskOrder
#
# class PaperAdmin(admin.ModelAdmin):
#     inlines = [TaskOrderInline]

class SourceAdmin(admin.ModelAdmin):
    form = SourceAdminForm

    def get_changelist_form(self, request, **kwargs):
        return SourceAdminForm

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Topic)
admin.site.register(Submit)
admin.site.register(Source, SourceAdmin)
admin.site.register(Paper)
admin.site.register(Variant)
# admin.site.register(TaskOrder)
admin.site.register(TestSet)
admin.site.register(TestSetAssignment)
admin.site.register(TestSubmit)
admin.site.register(GroupTeacher)
admin.site.register(PaperAssignment)
admin.site.register(Theory)
admin.site.register(PaperObject)