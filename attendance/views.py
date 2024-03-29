from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import LoginForm
from .forms import semForm
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import selenium
import time
import pandas as pd
from bs4 import BeautifulSoup
from django import forms
import ast
from datetime import date, datetime
from .models import User

demoData=[
{'Name': 'Chemistry', 'Count': '37/41', 'Percentage': 90.24},
{'Name': 'Chemistry Lab', 'Count': '7/7', 'Percentage': 100.0},
{'Name': 'Object Oriented Programming', 'Count': '25/35', 'Percentage': 71.42},
{'Name': 'Object Oriented Programming Lab', 'Count': '4/9', 'Percentage': 44.44},
{'Name': 'Operating Systems', 'Count': '27/33', 'Percentage': 81.82},
{'Name': 'Operating Systems Lab', 'Count': '20/20', 'Percentage': 100.0},
{'Name': 'Systems Lab-II', 'Count': '13/15', 'Percentage': 86.67},
{'Name': 'Data Science Programming', 'Count': '29/34', 'Percentage': 85.29}
]

def index(request):
    context={}
    context['form'] = LoginForm()
    return render( request, "index.html", context) 

def semester(request):
    context={}
    context['form'] = semForm()
    return render( request, "index.html", context) 

def addInput(driver, by, value, text):
    field = driver.find_element(by=by, value=value)
    field.send_keys(text)

def clickButton(driver, by, value):
    button = driver.find_element(by=by, value=value)
    button.click()
    
def loginRCOEM(driver, username, password):
    addInput(driver, By.ID, 'j_username', username)
    addInput(driver, By.ID, 'password-1', password)
    clickButton(driver, By.CLASS_NAME, 'btn.btn-primary.btn-block.customB.mt-3')
    return username
    
# def get_attendance(driver):
#     click_button(driver, By.ID,'attendencePer')
# def select_sem(driver, term_value):
#         term_dropdown = Select(driver.find_element(By.ID, 'termId'))
#         term_dropdown.select_by_value(term_value)
#
# def click_attendance(driver, label_text):
#     label_xpath = f"//label[text()='{label_text}']"
#     label = driver.find_element(By.XPATH, label_xpath)
#     driver.execute_script("arguments[0].click();", label)
#
# def attendance_div(driver):
#     attendanceDiv = driver.find_element(By.ID, 'attendanceDiv').get_attribute('outerHTML')
#     return attendanceDiv


def error_page(request):
    context={}
    context['form'] = LoginForm()
    return render(request, 'error.html', context)

def getAttendance(jsonFile, sem):
    data = []

    totalPresent, totalAbsent, percent, finalCount =0,0,0,0

    for i in range(len(jsonFile.json())):
        if jsonFile.json()[i]['termId'] == sem:
            sub = jsonFile.json()[i]['subject']
            absent = jsonFile.json()[i]['absentCount']
            present = jsonFile.json()[i]['presentCount']
            totalPresent += present
            totalAbsent += absent 
            if(totalAbsent == 0 or totalPresent == 0):
                continue
            else:
                finalCount = f"{totalPresent}/{totalAbsent+totalPresent}"
                percent = round((totalPresent/(totalAbsent+totalPresent))*100, 2)
                if absent+present == 0:
                    percentage = 0
                else:
                    percentage = round((present/(absent+present))*100, 2)    
            data.append({
                'Name' : sub,
                'Count' : f"{present}/{absent+present}",
                'Percentage' :  percentage
            })
            
    return(data, percent, finalCount)


def loginDetails(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data.get('username')
            password = loginform.cleaned_data.get('password')
            
            if(username == 'demo@rknec.edu' and password == 'demo@rknec.edu'):
                context = {'username':username, 'demo':True, 'cookies' : None}
                user = User(userID = username)
                user.save()
            else:    
                options = webdriver.ChromeOptions()
                prefs = {"profile.managed_default_content_settings.images": 2}
                options.add_experimental_option("prefs", prefs)
                options.add_argument('--headless')
                chrome_driver_path = ChromeDriverManager().install()
                driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
                driver.get("https://rcoem.in/login.htm")

                usernameID = loginRCOEM(driver, username, password)
            
                if 'failure=true' in driver.current_url:
                    return redirect('error_page')
                else:
                    cookies = driver.get_cookies()
                    context = {'cookies':cookies}
                    context['form'] = semForm()
                    context['demo'] = False
                    context['username'] = usernameID
                    user = User(userID = username)
                    user.save()
                    #   print(cookies)
                driver.quit()
    return render(request, 'semester.html', context)

def displayAttendance(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        # print('demo = ' + demo)
        if userID == 'demo@rknec.edu':
            print('demo user')
            context = {'table': demoData, 'percentFinal': 83.51, 'countFinal': '162/194', 'userID': 'demo@rknec.edu'}
        else:
            print('normal user')
            semform = semForm(request.POST)
            cookiesStr = request.POST.get('cookies')
            userID = request.POST.get('userID')
            
            if semform.is_valid():
                cookies_list = ast.literal_eval(cookiesStr)
                sem = int(semform.cleaned_data['semester'])
                attendancdeJSON = requests.get('https://rcoem.in/getSubjectOnChangeWithSemId1.json?', headers={'accept': 'application/json', 'Cookie': 'JSESSIONID=' + cookies_list[0]['value']})
                table, percent, count = getAttendance(attendancdeJSON, sem)
                
                if len(table) != 0:
                    context = {'table': table, 'percentFinal': percent, 'countFinal': count, 'userID': userID}
                else:
                    context = {'nullData': 'No data to display'}

    return render(request, "result.html", context)

# def displayAttendance(request):
#     if request.method == 'POST':
#         demo  =request.POST.get('demo')
#         if not demo:
#             semform = semForm(request.POST)
#             cookiesStr  =request.POST.get('cookies')
#             userID  =request.POST.get('userID')
#             # print(cookiesStr)
#             if semform.is_valid():
#                 cookies_list = ast.literal_eval(cookiesStr)
#                 sem = int(semform.cleaned_data['semester'])
#                 attendancdeJSON = requests.get('https://rcoem.in/getSubjectOnChangeWithSemId1.json?', headers = {'accept': 'application/json', 'Cookie':'JSESSIONID='+cookies_list[0]['value']})
#                 table,percent,count = getAttendance(attendancdeJSON, sem)
#             # print(table)
#                 if len(table)!=0:    
#                     context = {'table':table, 'percentFinal':  percent, 'countFinal':count, 'userID': userID}
#                 else:
#                     context = {'nullData':'No data to display'}
#         else:
#             print('demo')
            
#             context = {'table' : demoData, 'percentFinal' : 86.34, 'countFinal':'196/227', 'userID': 'demo@rknec.edu'}
        
#     return render(request, "result.html", context)
