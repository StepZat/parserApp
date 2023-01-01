from django.contrib import admin
from .models import Vacancy, Area, ChildRole, Schedule, Experience, Employment, EducationLevel

# Register your models here.


admin.site.register(Vacancy)
admin.site.register(Area)
admin.site.register(ChildRole)
admin.site.register(Employment)
admin.site.register(Experience)
admin.site.register(Schedule)
admin.site.register(EducationLevel)


