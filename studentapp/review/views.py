from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from review.models import HelpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def student_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, 'signup.html', {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {"error": "Username already taken"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_staff = False  # Ensure not staff
        user.save()

        login(request, user)
        return redirect('review_dashboard')

    return render(request, 'signup.html')

def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_staff:
                return render(request, 'login.html', {"error": "Staff cannot log in here."})
            login(request, user)
            return redirect('review_dashboard')
        else:
            return render(request, 'login.html', {"error": "Invalid credentials"})
    return render(request, 'login.html')

@login_required
def review_dashboard(request):
    return render(request, 'review.html')

@csrf_exempt
@login_required
def submit_help_request(request):
    if request.method == "POST":
        request_type = request.POST.get("type")
        message = request.POST.get("message", "")
        
        HelpRequest.objects.create(
            student=request.user,
            request_type=request_type,
            message=message
        )
        return JsonResponse({"status": "success", "message": "Request submitted!"})
    return JsonResponse({"status": "error", "message": "Invalid request."})

@login_required
def user_logout(request):
    logout(request)
    return redirect('student_login')
