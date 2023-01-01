import requests
from time import sleep
from datetime import *
from dateutil.relativedelta import relativedelta
from .models import Vacancy
URL_VAC = "https://api.hh.ru/vacancies"
PER_PAGE = 100


def generateDays():
    first_date = (datetime.now() - relativedelta(months=1)).date()
    last_date = datetime.now().date()
    date_range = []
    for n in range(int((last_date - first_date).days) + 1):
        date_range.append((first_date + timedelta(n)).strftime("%Y-%m-%d"))
    return date_range


def generateHours(day):
    hours = []
    for hour in range(24):
        if hour < 10:
            hours.append(f"{day}T0{hour}:00:00")
        else:
            hours.append(f"{day}T{hour}:00:00")
    next_day = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    hours.append(f"{next_day}T00:00:00")
    return hours


def generateHalfHours(day):
    halfHours = []
    for hour in range(24):
        if hour < 10:
            date00 = f"{day}T0{hour}:00:00"
            halfHours.append(date00)
            date30 = (datetime.strptime(f"{day}T0{hour}:00:00", "%Y-%m-%dT%H:%M:%S") + relativedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")
            halfHours.append(date30)
    next_day = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    halfHours.append(f"{next_day}T00:00:00")
    return halfHours


def getVacanciesInfoHalfHour(day, params):
    global vacSlrFrom, vacSlrTo
    halfHours = generateHalfHours(day)
    for i in range(len(halfHours)-1):
        params["date_from"] = halfHours[i]
        params["date_to"] = halfHours[i + 1]
        response = requests.get(
            url=URL_VAC,
            params=params
        )
        json_vacs = response.json()
        response.close()
        sleep(0.25)
        pages = json_vacs["pages"]
        for page in range(pages):
            params["page"] = page
            responseList = requests.get(
                url=URL_VAC,
                params=params
            )
            json_vacs_list_items = responseList.json()["items"]
            responseList.close()
            sleep(0.25)
            for item in json_vacs_list_items:
                vacId = item["id"]
                vacName = item["name"]
                vacArea = item["area"]["name"]
                vacEmployer = item["employer"]["name"]
                vacSchedule = item["schedule"]["name"]
                if item["salary"] is None:
                    vacSlrFrom = None
                    vacSlrTo = None
                else:
                    if item["salary"]["from"] is None:
                        vacSlrFrom = None
                    else:
                        vacSlrFrom = item["salary"]["from"]
                    if item["salary"]["to"] is None:
                        vacSlrTo = None
                    else:
                        vacSlrTo = item["salary"]["to"]
                vacDescr = item["snippet"]["responsibility"]
                vacPubDate = item["published_at"]
                vac = Vacancy(
                    vac_id=vacId,
                    vac_name=vacName,
                    area_id=vacArea,
                    employer_name=vacEmployer,
                    vac_schedule=vacSchedule,
                    salary_from=vacSlrFrom,
                    salary_to=vacSlrTo,
                    description=vacDescr,
                    publication_date=vacPubDate
                )
                vac.save()


def getVacanciesInfoHour(day, params):
    global vacSlrFrom, vacSlrTo
    hours = generateHours(day)
    for i in range(len(hours)-1):
        params["date_from"] = hours[i]
        params["date_to"] = hours[i + 1]
        response = requests.get(
            url=URL_VAC,
            params=params
        )
        json_vacs = response.json()
        response.close()
        sleep(0.25)
        found = json_vacs["found"]
        if found > 2000:
            getVacanciesInfoHalfHour(day, params)
        else:
            pages = json_vacs["pages"]
            for page in range(pages):
                params["page"] = page
                responseList = requests.get(
                    url=URL_VAC,
                    params=params
                )
                json_vacs_list_items = responseList.json()["items"]
                responseList.close()
                sleep(0.25)
                for item in json_vacs_list_items:
                    vacId = item["id"]
                    vacName = item["name"]
                    vacArea = item["area"]["name"]
                    vacEmployer = item["employer"]["name"]
                    vacSchedule = item["schedule"]["name"]
                    if item["salary"] is None:
                        vacSlrFrom = None
                        vacSlrTo = None
                    else:
                        if item["salary"]["from"] is None:
                            vacSlrFrom = None
                        else:
                            vacSlrFrom = item["salary"]["from"]
                        if item["salary"]["to"] is None:
                            vacSlrTo = None
                        else:
                            vacSlrTo = item["salary"]["to"]
                    vacDescr = item["snippet"]["responsibility"]
                    vacPubDate = item["published_at"]
                    vac = Vacancy(
                        vac_id=vacId,
                        vac_name=vacName,
                        area_id=vacArea,
                        employer_name=vacEmployer,
                        vac_schedule=vacSchedule,
                        salary_from=vacSlrFrom,
                        salary_to=vacSlrTo,
                        description=vacDescr,
                        publication_date=vacPubDate
                    )
                    vac.save()


def getVacanciesInfoDay(params):
    global vacSlrFrom, vacSlrTo
    days = generateDays()
    for i in range(len(days)):
        params["date_from"] = days[i]
        params["date_to"] = days[i]
        responseDays = requests.get(
            url=URL_VAC,
            params=params
        )
        json_vacs = responseDays.json()
        responseDays.close()
        sleep(0.25)
        found = json_vacs["found"]
        if found > 2000:
            getVacanciesInfoHour(days[i], params)
        else:
            pages = json_vacs["pages"]
            for page in range(pages):
                params["page"] = page
                responseList = requests.get(
                    url=URL_VAC,
                    params=params
                )
                json_vacs_list_items = responseList.json()["items"]
                responseList.close()
                sleep(0.25)
                for item in json_vacs_list_items:
                    vacId = item["id"]
                    vacName = item["name"]
                    vacArea = item["area"]["name"]
                    vacEmployer = item["employer"]["name"]
                    vacSchedule = item["schedule"]["name"]
                    if item["salary"] is None:
                        vacSlrFrom = None
                        vacSlrTo = None
                    else:
                        if item["salary"]["from"] is None:
                            vacSlrFrom = None
                        else:
                            vacSlrFrom = item["salary"]["from"]
                        if item["salary"]["to"] is None:
                            vacSlrTo = None
                        else:
                            vacSlrTo = item["salary"]["to"]
                    vacDescr = item["snippet"]["responsibility"]
                    vacPubDate = item["published_at"]
                    vac = Vacancy(
                        vac_id=vacId,
                        vac_name=vacName,
                        area_id=vacArea,
                        employer_name=vacEmployer,
                        vac_schedule=vacSchedule,
                        salary_from=vacSlrFrom,
                        salary_to=vacSlrTo,
                        description=vacDescr,
                        publication_date=vacPubDate
                    )
                    vac.save()


def getVacanciesInfoAll(params):
    global vacSlrFrom, vacSlrTo
    response = requests.get(
        url=URL_VAC,
        params=params
    )
    json_vacs = response.json()
    print(response.url)
    response.close()
    sleep(0.25)
    found = json_vacs["found"]
#    vacs = []
    if found > 2000:
        getVacanciesInfoDay(params)
    else:
        pages = json_vacs["pages"]
        for page in range(pages):
            params["page"] = page
            responseList = requests.get(
                url=URL_VAC,
                params=params
            )
            json_vacs_list_items = responseList.json()["items"]
            responseList.close()
            sleep(0.25)
            for item in json_vacs_list_items:
                vacId = item["id"]
                vacName = item["name"]
                vacArea = item["area"]["name"]
                vacEmployer = item["employer"]["name"]
                vacSchedule = item["schedule"]["name"]
                if item["salary"] is None:
                    vacSlrFrom = None
                    vacSlrTo = None
                else:
                    if item["salary"]["from"] is None:
                        vacSlrFrom = None
                    else:
                        vacSlrFrom = item["salary"]["from"]
                    if item["salary"]["to"] is None:
                        vacSlrTo = None
                    else:
                        vacSlrTo = item["salary"]["to"]
                vacDescr = item["snippet"]["responsibility"]
                vacPubDate = item["published_at"]
                vac = Vacancy(
                    vac_id=vacId,
                    vac_name=vacName,
                    area_id=vacArea,
                    employer_name=vacEmployer,
                    vac_schedule=vacSchedule,
                    salary_from=vacSlrFrom,
                    salary_to=vacSlrTo,
                    description=vacDescr,
                    publication_date=vacPubDate
                )
                vac.save()


def deleteUseless(params):
    for key, value in params.copy().items():
        if value is None or value == "":
            params.pop(key)
    return params
