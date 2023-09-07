from django.contrib import admin
from .models import Exercise, ExerciseSet,Workout,CalCount,ProteinCal

# Register your models here.

admin.site.register(Exercise)
admin.site.register(ExerciseSet)
admin.site.register(CalCount)
admin.site.register(ProteinCal)

class ExerciseSetInline(admin.TabularInline):
    model = ExerciseSet

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [ExerciseSetInline]

admin.site.register(Workout, WorkoutAdmin)
