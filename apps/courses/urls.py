from django.urls import path
from .views import CourseListView, CourseCreateView, CourseDetailView, LessonListView, LessonCreateView, EnrollView, \
    MyEnrollmentsView, ReviewListCreateView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/add/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Lessons
    path('courses/<int:course_id>/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('courses/<int:course_id>/lessons/add/', LessonCreateView.as_view(), name='lesson-add'),

    # Enrollment
    path('courses/<int:course_id>/enroll/', EnrollView.as_view(), name='course-enroll'),
    path('my-enrollments/', MyEnrollmentsView.as_view(), name='my-enrollments'),

    # Reviews
    path('courses/<int:course_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
]
