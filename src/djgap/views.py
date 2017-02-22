from django.shortcuts import render


def home(request):
	return render(request, "index.html", {})

def courses(request):
	return render(request, "courses.html", {})

def dashboard(request):
	return render(request, "dashboard.html", {})
