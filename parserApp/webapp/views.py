import codecs
import csv
from datetime import datetime

import requests
from time import sleep
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.template import loader
from django.views import View

from .forms import ParserForm
from .models import Area, ChildRole, Experience, Employment, EducationLevel, Schedule, Vacancy
from .vacancy_script import getVacanciesInfoAll, deleteUseless

URL_AREAS = "https://api.hh.ru/areas"
URL_ROLES = "https://api.hh.ru/professional_roles"
URL_DICTS = "https://api.hh.ru/dictionaries"


@login_required(login_url='/users/login/')
def start(request):
    return render(request, 'parser/parser.html')


def about(request):
    return render(request, 'parser/parser.html')

@login_required(login_url='/users/login/')
def query(request):
    form = ParserForm()
    if request.method =='POST':
        form = ParserForm(request.POST)
        if form.is_valid():
            params = {"text": form.cleaned_data.get("query_text"),
                      "area": form.data.get("region"),
                      "experience": form.data.get("expr"),
                      "employment": form.data.get("empl"),
                      "schedule": form.data.get("schedl"),
                      "professional_role": form.cleaned_data.get("jobs").values_list("role_id", flat=True),
                      "per_page": 100,
                      "page": 0}
            Vacancy.objects.all().delete()
            params = deleteUseless(params)
            getVacanciesInfoAll(params=params)
            return redirect('/parser/result')
    data = {
        'form': form
    }
    return render(request, 'parser/query.html', data)


def uploadRegions():
    Area.objects.all().delete()
    response = requests.get(URL_AREAS)
    data = response.json()[0]["areas"]
    response.close()
    for area in data:
        areaID = area["id"]
        areaName = area["name"]
        region = Area(area_id=areaID, area_name=areaName)
        region.save()


def uploadRoles():
    ChildRole.objects.all().delete()
    response = requests.get(URL_ROLES)
    data = response.json()["categories"]
    for parentRole in data:
        parentRoleRoles = parentRole["roles"]
        for child_role in parentRoleRoles:
            roleID = child_role["id"]
            roleName = child_role["name"]
            ch_role = ChildRole(role_id=roleID,
                                role_name=roleName)
            ch_role.save()

@login_required(login_url='/users/login/')
def uploadDicts(request):
    uploadRegions()
    uploadRoles()
    Experience.objects.all().delete()
    Employment.objects.all().delete()
    EducationLevel.objects.all().delete()
    Schedule.objects.all().delete()
    response = requests.get(URL_DICTS)
    data = response.json()
    response.close()
    experience = data["experience"]
    for exp in experience:
        exp_id = exp["id"]
        exp_name = exp["name"]
        exper = Experience(exp_id=exp_id,
                           exp_name=exp_name)
        exper.save()
    employment = data["employment"]
    for emp in employment:
        emp_id = emp["id"]
        emp_name = emp["name"]
        employ = Employment(emp_id=emp_id,
                            emp_name=emp_name)
        employ.save()
    education_level = data["education_level"]
    for el in education_level:
        el_id = el["id"]
        el_name = el["name"]
        e_level = EducationLevel(el_id=el_id,
                                 el_name=el_name)
        e_level.save()
    schedule = data["schedule"]
    for schd in schedule:
        schd_id = schd["id"]
        schd_name = schd["name"]
        schedl = Schedule(schd_id=schd_id,
                          schd_name=schd_name)
        schedl.save()
    return render(request, 'parser/uploaddicts.html')

@login_required(login_url='/users/login/')
def load_vacancies(request):
    vacs = Vacancy.objects.all()
    avg_salary = count_avg_salary()
    page = request.GET.get('page', 1)
    paginator = Paginator(vacs, 20)
    try:
        vacancies = paginator.page(page)
    except PageNotAnInteger:
        vacancies = paginator.page(1)
    except EmptyPage:
        vacancies = paginator.page(paginator.num_pages)
    params = {
        'vacs': vacs,
        'vacancies': vacancies,
        'avg_salary': avg_salary
    }
    return render(request, 'parser/result.html', params)


def count_avg_salary():
    salaries_from = Vacancy.objects.all().values_list('salary_from', flat=True)
    salaries_to = Vacancy.objects.all().values_list('salary_to', flat=True)
    avgs = []
    for sal in range(Vacancy.objects.count()):
        if (salaries_from[sal] is not None) and (salaries_to[sal] is not None):
            avgs.append((salaries_from[sal]+salaries_to[sal])/2)
        elif (salaries_from[sal] is not None) and (salaries_to[sal] is None):
            avgs.append(salaries_from[sal])
        elif (salaries_from[sal] is None) and (salaries_to[sal] is not None):
            avgs.append(salaries_to[sal])
    average_salary = int(sum(avgs)/len(avgs))
    return average_salary


def export_to_csv_windows(request):
    vacs = Vacancy.objects.all()
    filename = f"vacancies_export_{datetime.today().strftime('%Y-%m-%d')}.csv"
    # with open(filename, 'w', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['ID', 'Вакансия', 'Регион', 'Работодатель', 'Расписание', 'Зарплата от', 'Зарплата до', 'Описание', 'Дата публикации'])
    #     data = vacs.values_list('vac_id', 'vac_name', 'area_id', 'employer_name', 'vac_schedule', 'salary_from',
    #                             'salary_to', 'description', 'publication_date')
    #     for line in data:
    #         writer.writerow(line)
    # with open(filename, 'r', encoding='utf-8') as file:
    #     file_data = file.read()
    # response = HttpResponse(file_data, content_type='text/csv; charset=cp1251')
    # response['Content-Disposition'] = f"attachment; filename={filename}"
    response = HttpResponse(content_type='text/csv; charset=cp1251')
    response['Content-Disposition'] = f"attachment; filename={filename}"
    writer = csv.writer(response)
    writer.writerow(['ID', 'Вакансия', 'Регион', 'Работодатель', 'Расписание', 'Зарплата от', 'Зарплата до', 'Описание', 'Дата публикации'])
    data = vacs.values_list('vac_id', 'vac_name', 'area_id', 'employer_name', 'vac_schedule', 'salary_from', 'salary_to', 'description', 'publication_date')
    for line in data:
       writer.writerow(line)
    return response


def export_to_csv_unix(request):
    vacs = Vacancy.objects.all()
    filename = f"vacancies_export_{datetime.today().strftime('%Y-%m-%d')}.csv"
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename={filename}"
    writer = csv.writer(response)
    writer.writerow(['ID', 'Вакансия', 'Регион', 'Работодатель', 'Расписание', 'Зарплата от', 'Зарплата до', 'Описание', 'Дата публикации'])
    data = vacs.values_list('vac_id', 'vac_name', 'area_id', 'employer_name', 'vac_schedule', 'salary_from', 'salary_to', 'description', 'publication_date')
    for line in data:
        writer.writerow(line)
    return response


