from django.shortcuts import render, Http404
from courses.models import Courses

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

# def course_update(request, course_id):
#     context = {}
#     try:
#         course = Courses.objects.get(id=course_id)
#         context["course"] = course
#     except:
#         context["error"] = 'Course not found'
#     return render (request, 'courses/update.html', context)