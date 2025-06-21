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
    
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import CourseSerializer
from .models import Courses

@api_view(['GET'])
def course_list_api(request):
    courses = Courses.objects.all()
    courses_json = CourseSerializer(courses, many=True)
    return Response(data=courses_json.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def course_detail_api(request, course_id):
    try:
        course = Courses.objects.get(pk=course_id)
        course_json = CourseSerializer(course)
        return Response(data=course_json.data, status=status.HTTP_200_OK)
    except:
        return Response(data={"msg": "course not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def course_delete_api(request, course_id):
    try:
        course = Courses.objects.get(pk=course_id)
        course.delete()
        return Response(data={"msg": f"course {course_id} deleted"}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(data={"msg": "course not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def course_update_api(request, course_id):
    try:
        course = Courses.objects.get(pk=course_id)
        data = CourseSerializer(course, data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={"msg": f"course with id: {course_id} updated successfully"}, status=status.HTTP_200_OK)
    except:
        return Response(data={"msg": "can't update"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def course_create_api(request):
    data = CourseSerializer(data=request.data)
    if data.is_valid():
        data.save()
        return Response(data={"msg": "course created successfully"}, status=status.HTTP_201_CREATED)
    # return Response(data={"msg": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)