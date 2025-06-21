from django.shortcuts import render, Http404
from courses.models import Courses
from .forms import CourseForm
from django.shortcuts import redirect

# courses = [
#     {'id': 1, 'name': 'Python'},
#     {'id': 2, 'name': 'C++'},
#     {'id': 3, 'name': 'Java'},
#     {'id': 4, 'name': 'HTML'},
#     {'id': 5, 'name': 'CSS'},
#     {'id': 6, 'name': 'JavaScript'},
# ]

def course_list(request):
    courses = Courses.objects.all()
    return render(request, 'courses/index.html', {'courses': courses})

# def course_detail(request, course_id):
#     for course in courses:
#         if course['id'] == course_id:
#             return render(request, 'courses/detail.html', {'course': course})
#     raise Http404("Course not found")

def course_detail(request, course_id):
    try:
        course = Courses.objects.get(id=course_id)
        context = {'course': course}
    except:
        context= {'error': 'Course not found'}
    return render (request, 'courses/detail.html', context)

def course_delete(request, course_id):
    context = {}
    try:
        course = Courses.objects.get(id=course_id)
        course.delete()
    except Courses.DoesNotExist:
        context["error"] = 'Course not found'
    context["courses"] = Courses.objects.all()
    return render(request, 'courses/index.html', context)

def course_update(request, course_id):
    try:
        course = Courses.objects.get(id=course_id)
        if request.method == "GET":
            form = CourseForm(initial={
                'name': course.name,
                'image': course.image,
            })
            return render(request, 'courses/create.html', {"form": form})
        else:
            form = CourseForm(request.POST, request.FILES)
            if 'image' not in request.FILES:
                form.data = form.data.copy()
                form.files['image'] = course.image
            if form.is_valid():
                course.name = form.cleaned_data['name']
                course.image = form.cleaned_data['image']
                course.save()
                return redirect("course-list")
            else:
                return render(request, 'courses/create.html', {"form": form, "error": "Please correct the data."})
    except:
        return redirect("course-list")

def course_create(request):
    if request.method == "GET":
        form= CourseForm()
        return render (request , 'courses/create.html' , {"form":form})
    else:
        data = CourseForm (request.POST , request.FILES)
        if data.is_valid():
            new_obj = Courses()
            new_obj.name = data.cleaned_data['name']
            new_obj.image = request.FILES['image']
            new_obj.save()
        return redirect ("course-list")