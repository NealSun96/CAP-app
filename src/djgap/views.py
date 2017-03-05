from django.shortcuts import render


def home(request):
	return render(request, "index.html", {})

def courses(request, key=""):
	return render(request, "courses.html", {"key": key})

def dashboard(request, id=""):
	return render(request, "dashboard.html", {"id": id})
