import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse

# 1. Config Django Settings แบบเขียนสดในไฟล์เดียว
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='secret-key-for-dev',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.getcwd()], # ให้หาไฟล์ html ในโฟลเดอร์ปัจจุบัน
            'APP_DIRS': True,
        }],
    )

# 2. View Logic (จัดการการคำนวณและการเปลี่ยนหน้า)
def index(request):
    context = {}
    page = request.GET.get('page', 'home') # อ่านค่า ?page=... ถ้าไม่มีให้เป็น home

    # ถ้ามีการกดคำนวณ (POST)
    if request.method == 'POST':
        try:
            glucose = int(request.POST.get('glucose', 0))
            weight = float(request.POST.get('weight', 0))
            height = float(request.POST.get('height', 0))

            # คำนวณ BMI
            bmi = 0
            if height > 0:
                bmi = weight / ((height / 100) ** 2)

            # Logic ประเมินผล
            status = "ปกติ"
            status_color = "#2ECC71" # เขียว
            if glucose > 140:
                status = "ผิดปกติ"
                status_color = "#E74C3C" # แดง
            elif glucose < 70:
                status = "ต่ำเกินไป"
                status_color = "#F39C12" # ส้ม

            context.update({
                'result_mode': True,
                'glucose': glucose,
                'weight': weight,
                'height': height,
                'bmi': round(bmi, 1),
                'status': status,
                'status_color': status_color,
                'page': 'result' # บังคับไปหน้าผลลัพธ์
            })
            return render(request, 'index.html', context)
        except:
            context['error'] = "กรุณากรอกตัวเลข"

    # ส่งตัวแปร page ไปบอก html ว่าจะโชว์หน้าไหน
    context['page'] = page
    return render(request, 'index.html', context)

# 3. URL Patterns
urlpatterns = [
    path('', index),
]

# 4. Main Execution
if __name__ == "__main__":
    execute_from_command_line(sys.argv)
