from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Enrollment, Review, Instructor
from .serializers import (
    CourseSerializer, LessonSerializer,
    EnrollmentSerializer, ReviewSerializer
)


# ----------------------------
# KURSLAR
# ----------------------------

# Kurslar ro'yxati
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


# Kurs qo'shish (faqat o'qituvchi)
class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'instructor':
            raise PermissionError("Faqat o'qituvchilar kurs qo'sha oladi")

        # Instructor profili mavjud bo'lmasa, yaratib yuboramiz
        instructor, created = Instructor.objects.get_or_create(user=user)
        serializer.save(instructor=instructor)


# Kurs detali
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


# ----------------------------
# DARSLAR
# ----------------------------

# Kursdagi barcha darslar
class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)


# Yangi dars qo'shish (o'qituvchi tomonidan)
class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)

        if self.request.user != course.instructor.user:
            raise PermissionError("Faqat shu kurs o‘qituvchisi dars qo‘sha oladi")

        serializer.save(course=course)


# ----------------------------
# ENROLLMENT (kursga yozilish)
# ----------------------------

class EnrollView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)
        user = self.request.user
        serializer.save(user=user, course=course)


# Foydalanuvchining yozilgan kurslari
class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)


# ----------------------------
# REVIEW (kursga sharh qoldirish)
# ----------------------------

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Review.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)
        serializer.save(user=self.request.user, course=course)
