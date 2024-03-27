from django.shortcuts import render,redirect
import csv
import time
from .forms import FileUpload
from .models import Recipient
import os 
import pywhatkit 
import pyautogui

def home(request):
    return render(request,"main/home.html")


def send(request):
    if request.method == 'POST':
        form = FileUpload(request.POST,request.FILES)
        if request.POST.get("send"):
            Recipient.objects.all().delete() #first delete earlier  versions recipient.csv for none first time users
            file = form.save()
            fileName = request.FILES['file']

            return redirect('sending')

            

    else:
        form = FileUpload()
        return render(request,'main/send.html',{"form":form})


msg = """I hope this message finds you well.  I noticed your business  doesn't have an online presence yet, and I believe a website could greatly benefit you.

In today's digital age, having a professional website is essential for reaching more customers and growing your brand. I specialize in creating custom websites that are tailored to meet the unique needs of businesses like yours.

I would love to discuss how I can help bring your vision to life at an affordable price. If interested let me know and we can explore  the possibilities.

Looking forward to hearing from you soon.

Prices start from as low as Ksh. 3500"""


def sending(request):
    status = ["Waiting to start"]
    if request.method == 'POST':
        if request.POST['send']:
            file_ = Recipient.objects.all()[0].file

            file_.path.strip()


            with open(file_.path,"r") as file:
                reader = csv.DictReader(file,delimiter=",")
                

                for row in reader:
                    status.append("Starting")
                    number = row["NUMBER"]
                    
                    pywhatkit.sendwhatmsg_instantly(number,msg,60) # Sends the message

                    status.append("Preparing to send message.Please don't move your mouse!!")
                    time.sleep(15)

                    pyautogui.click() # Clicks the bar
                    pyautogui.press('enter') # Sends the message
                    status.append(f"Message sent to {number}.Preparing other recipients")

                    time.sleep(5)

                status.append("All messages have been sent!!")

        return render(request,'main/sending.html',{"status":status})

    return render(request,'main/sending.html',{"status":status})