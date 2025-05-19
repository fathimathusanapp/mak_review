from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from review.models import HelpRequest
from django.contrib.auth import authenticate, login


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/staff/login/')
def help_requests_view(request):
    help_requests = HelpRequest.objects.order_by('-created_at').select_related('student', 'accepted_by')
    return render(request, 'help_requests.html', {'help_requests': help_requests})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/staff/login/')
def accept_help_request(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)
    if not help_request.accepted_by:  # accept only if not accepted
        help_request.accepted_by = request.user
        help_request.save()
    return redirect('staff_help_requests')

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/staff/login/')
def mark_request_handled(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)
    if help_request.accepted_by == request.user:
        help_request.is_handled = True
        help_request.save()
    return redirect('staff_help_requests')

def staff_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_staff:
                return render(request, 'staff_login.html', {"error": "Students cannot log in here."})
            login(request, user)
            return redirect('staff_help_requests')
        else:
            return render(request, 'staff_login.html', {"error": "Invalid credentials"})
    return render(request, 'staff_login.html')

