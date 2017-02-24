from django.shortcuts import render


def home(request):
	return render(request, "index.html", {})

def courses(request, key = ""):
	return render(request, "courses.html", {"key": key})

def dashboard(request):
	return render(request, "dashboard.html", {})
