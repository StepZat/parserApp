from django.db import models

# Create your models here.


class Vacancy(models.Model):
    vac_id = models.IntegerField(primary_key=True)
    vac_name = models.CharField(max_length=255)
    area_id = models.CharField(max_length=255)
    employer_name = models.CharField(max_length=255)
    vac_schedule = models.CharField(max_length=32)
    salary_from = models.IntegerField(null=True)
    salary_to = models.IntegerField(null=True)
    description = models.TextField(null=True)
    publication_date = models.DateTimeField()


class Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=255)

    def __str__(self):
        return self.area_name


class Experience(models.Model):
    exp_id = models.CharField(primary_key=True, max_length=255)
    exp_name = models.CharField(max_length=255)

    def __str__(self):
        return self.exp_name


class EducationLevel(models.Model):
    el_id = models.CharField(primary_key=True, max_length=255)
    el_name = models.CharField(max_length=255)

    def __str__(self):
        return self.el_name


class Employment(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=255)
    emp_name = models.CharField(max_length=255)

    def __str__(self):
        return self.emp_name


class Schedule(models.Model):
    schd_id = models.CharField(primary_key=True, max_length=255)
    schd_name = models.CharField(max_length=255)

    def __str__(self):
        return self.schd_name


class ChildRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


