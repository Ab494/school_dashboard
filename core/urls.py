from atexit import register
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.dashboard, name='dashboard'),
    path("students/", views.students, name='students'),
    path('teachers/', views.teachers, name='teachers'),
    path("attendance/", views.attendance, name='attendance'),
    path("add_student/", views.add_student, name='add_student'),
    path("add_teacher/", views.add_teacher, name='add_teacher'),
    path("add_attendance/", views.add_attendance, name='add_attendance'),
    path("delete-student/<int:pk>/", views.delete_student, name='delete_student'),
    path("delete-teacher/<int:pk>/", views.delete_teacher, name='delete_teacher'),
    path("delete-attendance/<int:pk>/", views.delete_attendance, name='delete_attendance'),
    path('get_counts/', views.get_counts, name='get_counts'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('units/', views.units_list, name='unit'),
    path('units/<int:pk>/delete/', views.delete_unit, name='delete_unit'),
    path('units/add/', views.unit_add, name='add_unit'),
    path('units/', views.unit_list, name='unit_list'),
    path('units/edit/<int:unit_id>/', views.unit_edit, name='edit_unit'),
    path('units/delete/<int:unit_id>/', views.unit_delete, name='delete_unit'),
    path('attendance-summary/', views.attendance_summary, name='attendance_summary'),
    path('mission-vision/', views.static_mission_vision, name='mission_vision'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html',
                                                                   success_url='/password_changed_successfully/'), name='change_password'),
    path('password_changed_successfully/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_changed_success.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password_reset_done/'
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset_done/'
    ), name='password_reset_confirm'),

    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

]