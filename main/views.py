from django.shortcuts import render,redirect
import csv
import time
from .forms import FileUpload
from .models import Recipient,RecipientOneMany,RecipientMany
import os 
import pywhatkit 
import pyautogui
from pynput.keyboard import Key,Controller
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages




def home(request):
    return render(request,"main/home.html")


#this is the page that is shown for mobile devices
def mobile(request):
    return render(request,'main/mobile.html')


def send(request):

    if request.method == 'POST':
        form = FileUpload(request.POST,request.FILES)
        if request.POST.get("send"):
            Recipient.objects.all().delete() #first delete earlier  versions recipient.csv for none first time users
            file = form.save()
            fileName = request.FILES['file']

            #check if user has account if not check that file has no more that 15 recipients
            file_ = Recipient.objects.all()[0].file


            with open(file_.path,"r") as file:
                r = csv.reader(file,delimiter=',')
                reader = csv.DictReader(file,delimiter=",")
                headers = [row for row in r][0]

                required_headers = ['NUMBER','MESSAGE']




                #check if the uploaded file contains required columns;numbers and msg
                for header_ in required_headers:
                    if header_ not in headers:
                        missing_header = header_
                        msg = f"The uploaded file does not have {missing_header} column or uses the wrong format.Please include the column or use the correct format."
                        form = FileUpload()
                    
                        context = {"form":form,"msg":msg}

                        return render(request,'main/send.html',{"context":context})



                #check if the uploaded files contains extra headers;columns
                for header_ in headers:
                    if header_ not in required_headers:
                        extra_header = header_
                        msg = f"The uploaded file contains an extra column {extra_header}!.It is supposed to only have two columns,NUMBER and MESSAGE."

                        form = FileUpload()
                    
                        context = {"form":form,"msg":msg}

                        return render(request,'main/send.html',{"context":context})
                

                #check that users without accounts can't send to more that 15 recipients
                 #check if a column is missing a value
                rowCount = 0

                for row in reader:
                    if row['NUMBER'] == "":
                        msg = f"Row {rowCount} is missing a phone number!"
                        form = FileUpload()    

                        context = {"form":form,"msg":msg}

                        return render(request,'main/send.html',{"context":context})


                    elif row['MESSAGE'] == "":
                        msg = f"Row {rowCount} is missing a message!"

                        form = FileUpload()    

                        context = {"form":form,"msg":msg}

                        return render(request,'main/send.html',{"context":context})
                    rowCount += 1




                if rowCount > 15 and not request.user.is_authenticated:
                    msg = "This files contains more than 15 recipients which is more than a guest user can send.Please Log in or create and account to send to more recipients."
                    form = FileUpload()    

                    context = {"form":form,"msg":msg}

                    return render(request,'main/send.html',{"context":context})

                else:
                    return redirect("sending")

            

    else:
        form = FileUpload()
        context = {"form":form}
        return render(request,'main/send.html',{"context":context})


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
                    keyboard = Controller()
                    time.sleep(3)

                    #press ctrl + W to close the tab
                    keyboard.press(Key.ctrl)
                    keyboard.press('w')
                    keyboard.release('w')
                    keyboard.release(Key.ctrl)



                status.append("All messages have been sent!!")

        return render(request,'main/sending.html',{"status":status})

    return render(request,'main/sending.html',{"status":status})







def sendingToMany(request):
    status = ["Waiting to start"]
    
    if request.method == 'POST':  
        if request.POST.get('send'):
            file_ = Recipient.objects.all()[0].file
            msg = request.POST['message']

            file_.path.strip()


            with open(file_.path,"r") as file:
                reader = csv.DictReader(file,delimiter=",")

                for row in reader:
                    if "#" not in row['NUMBER']:
                        status.append("Starting")
                        number = row['NUMBER']
                        pywhatkit.sendwhatmsg_instantly(number,msg,60) # Sends the message

                        status.append("Preparing to send message.Please don't move your mouse!!")
                        time.sleep(15)

                        pyautogui.click() # Clicks the bar
                        pyautogui.press('enter') # Sends the message
                        status.append(f"Message sent to {number}.Preparing other recipients")
                        keyboard = Controller()
                        time.sleep(3)

                        #press ctrl + W to close the tab
                        keyboard.press(Key.ctrl)
                        keyboard.press('w')
                        keyboard.release('w')
                        keyboard.release(Key.ctrl)


                status.append("All messages have been sent!!")

        return render(request,'main/sendingToMany.html',{"status":status})

    return render(request,'main/sendingToMany.html',{"status":status})




@login_required
def customOneToMany(request):
    #get the custom one to many template file for downloading
    fileToMany_ = RecipientOneMany.objects.all()[0].file

    if request.method == 'POST':
        form = FileUpload(request.POST,request.FILES)
        if request.POST.get("sendToMany"):
            Recipient.objects.all().delete() #first delete earlier  versions recipient.csv for none first time users
            file = form.save()
            fileName = request.FILES['file']

            #check if user has account if not check that file has no more that 15 recipients
            file_ = Recipient.objects.all()[0].file


            with open(file_.path,"r") as file:
                r = csv.reader(file,delimiter=',')
                reader = csv.DictReader(file,delimiter=",")
                headers = [row for row in r][0]

                required_headers = ['NUMBER']

                #check if the uploaded file contains required columns;numbers and msg
                for header_ in required_headers:
                    if header_ not in headers:
                        missing_header = header_
                        msg = f"The uploaded file does not have {missing_header} column or uses the wrong format.Please include the column or use the correct format."
                        form = FileUpload()
                    
                        context = {"form":form,"msg":msg,'download_file':fileToMany_}

                        return render(request,'main/customOne2Many.html',{"context":context})

                        

                #check if the uploaded files contains extra headers;columns
                for header_ in headers:
                    if header_ not in required_headers:
                        extra_header = header_
                        msg = f"The uploaded file contains an extra column {extra_header}!.It is supposed to only have only a NUMBER column!."

                        form = FileUpload()
                    
                        context = {"form":form,"msg":msg,'download_file':fileToMany_}

                        return render(request,'main/customOne2Many.html',{"context":context})
                

                #check that users without accounts can't send to more that 15 recipients
                 #check if a column is missing a value
                rowCount = 0

                for row in reader:
                    if row['NUMBER'] == "":
                        msg = f"Row {rowCount} is missing a phone number!"
                        form = FileUpload()    

                        context = {"form":form,"msg":msg,'download_file':fileToMany_}
                        return render(request,'main/customOne2Many.html',{"context":context})


                    elif row['MESSAGE'] == "":
                        msg = f"Row {rowCount} is missing a message!"

                        form = FileUpload()    

                        context = {"form":form,"msg":msg,'download_file':fileToMany_}

                        return render(request,'main/customOne2Many.html',{"context":context})
                    rowCount += 1




                if rowCount > 50 and not request.user.is_authenticated:
                    msg = "This files contains more than 15 recipients which is more than a guest user can send.Please Log in or create and account to send to more recipients."
                    form = FileUpload()    

                    context = {"form":form,"msg":msg,'download_file':fileToMany_}

                    return render(request,'main/customOne2Many.html',{"context":context})

            return redirect("sendingToMany")
    else:
        form = FileUpload()    
        context = {'form':form,'download_file':fileToMany_}
        return render(request,'main/customOne2Many.html',{"context":context})



    
