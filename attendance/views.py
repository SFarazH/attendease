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

# f = open("./data.txt", "r")
# print(f.read())

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
    
# def get_attendance(driver):
#     click_button(driver, By.ID,'attendencePer')
# def select_sem(driver, term_value):
#         term_dropdown = Select(driver.find_element(By.ID, 'termId'))
#         term_dropdown.select_by_value(term_value)
# def click_attendance(driver, label_text):
#     label_xpath = f"//label[text()='{label_text}']"
#     label = driver.find_element(By.XPATH, label_xpath)
#     driver.execute_script("arguments[0].click();", label)
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
              context['username'] = usernameID
              
            #   print(cookies)
            driver.quit()
            return render(request, 'semester.html', context)

def displayAttendance(request):
    if request.method == 'POST':
      semform = semForm(request.POST)
      cookiesStr  =request.POST.get('cookies')
      # print(cookiesStr)
      if semform.is_valid():
        cookies_list = ast.literal_eval(cookiesStr)
        sem = int(semform.cleaned_data['semester'])
        attendancdeJSON = requests.get('https://rcoem.in/getSubjectOnChangeWithSemId1.json?', headers = {'accept': 'application/json', 'Cookie':'JSESSIONID='+cookies_list[0]['value']})
        
        table,percent,count = getAttendance(attendancdeJSON, sem)
        print(table)
        if len(table)!=0:    
          context = {'table':table, 'percentFinal':  percent, 'countFinal':count}
        else:
          context = {'nullData':'No data to display'}
        return render(request, "result.html", context)
