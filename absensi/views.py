from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Attendance, LeaveRequest, UserProfile

@login_required
def profile_detail(request):
    return render(request, 'absensi/profile_detail.html')

@csrf_exempt
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'absensi/change_password.html', {'form': form})

@login_required
def history(request):
    attendances = Attendance.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'absensi/history.html', {'attendances': attendances})

@login_required
def notifications(request):
    # Simpan notifikasi statis untuk sementara
    notif_list = [
        {'title': 'Absensi Berhasil', 'desc': 'Anda berhasil melakukan absen masuk hari ini.', 'time': 'Baru saja'},
        {'title': 'Info Cuti', 'desc': 'Pengajuan cuti Anda sedang ditinjau oleh admin.', 'time': '1 jam yang lalu'},
    ]
    return render(request, 'absensi/notifications.html', {'notifications': notif_list})
import base64
from django.core.files.base import ContentFile
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    attendances = Attendance.objects.filter(user=request.user).order_by('-timestamp')[:5]
    leaves = LeaveRequest.objects.filter(user=request.user).order_by('-created_at')[:3]
    return render(request, 'absensi/dashboard.html', {
        'attendances': attendances,
        'leaves': leaves
    })

@csrf_exempt
@login_required
def do_attendance(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        image_data = request.POST.get('image')

        # Convert base64 image to file
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f"absent_{request.user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}")

        Attendance.objects.create(
            user=request.user,
            foto=data,
            latitude=lat,
            longitude=lng,
            status=status
        )
        return JsonResponse({'status': 'success', 'message': f'Absensi {status} Berhasil!'})
    
    return render(request, 'absensi/attendance.html')

@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except:
        profile = UserProfile.objects.create(user=request.user)
    
    return render(request, 'absensi/profile.html', {'profile': profile})

@csrf_exempt
@login_required
def leave_request(request):
    if request.method == 'POST':
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        LeaveRequest.objects.create(
            user=request.user,
            tanggal_mulai=start,
            tanggal_selesai=end,
            alasan=reason
        )
        return redirect('dashboard')
        
    return render(request, 'absensi/leave_request.html')



@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
