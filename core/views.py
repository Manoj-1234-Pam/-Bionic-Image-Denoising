from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .decorators import *
from contact.models import *

import os
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Create your views here.
@login_required(login_url='login')
def home(request):
    try:
        if request.method == "POST":
            txt1 = request.POST['txt1']          
            txt2 = request.POST['txt2']          
            txt3 = request.POST['txt3']          
            txt4 = request.POST['txt4']          
            obj = Contact(
                email = txt1,
                phone = txt2,
                website = txt3,
                message = txt4,
                )
            obj.save()
    except:
        print('Error!.. Try Again Later')
        return  redirect('home')
    return render(request, 'home.html')


@login_required(login_url='login')

def predection(request):
    original_size = ''
    compressed_size = ''
    cpath = ''
    if request.method == "POST":
        txt1 = request.POST.get("txt1")
        txt2 = request.POST.get("txt2")
        # Get the desktop path
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        # Reading image from folder where it is stored
        img = cv2.imread(txt1)
        # Denoising the image and saving it into dst
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)

        # Creating a sharpening kernel
        sharpening_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        # Applying the sharpening kernel to the denoised image
        sharpened_img = cv2.filter2D(dst, -1, sharpening_kernel)

        # Save the denoised and sharpened image
        cv2.imwrite(os.path.join(desktop_path, 'sharpened_image.jpg'), sharpened_img)

        # Convert the images from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        dst_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        sharpened_img_rgb = cv2.cvtColor(sharpened_img, cv2.COLOR_BGR2RGB)

        # Plotting the source, denoised, and sharpened images
        plt.subplot(131), plt.imshow(img_rgb), plt.title('Original Image')
        plt.subplot(132), plt.imshow(dst_rgb), plt.title('Denoised Image')
        plt.subplot(133), plt.imshow(sharpened_img_rgb), plt.title('Sharpened Image')

        # Save the plot
        plt.savefig(os.path.join(desktop_path, txt2+'.jpg'))

        plt.show()
    return render(request, 'predection.html')


@unathenticated_user
def ac_login(request):
    if request.method == 'POST':
        username = request.POST.get('login-txt1')
        password = request.POST.get('login-txt2')
        try:
            lstatus = User.objects.get(username=username)
            if lstatus.is_active:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    print('Invalid Credentials..!')
            else:
                print('Contact Dean to activate Account')
        except:
            print('Invalid Credentials..!')
            return redirect ('login')
    return render (request, 'login.html')

def ac_logout(request):
    logout(request)
    return redirect('login')



