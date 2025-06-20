from django.shortcuts import render, redirect
from .models import Student, Teacher, Attendance
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import UnitForm, StudentForm
from .models import Unit
from django.db import IntegrityError

# Dashboard 

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_attendance = Attendance.objects.count()
    present_count = Attendance.objects.filter(status='present').count()
    absent_count = Attendance.objects.filter(status='absent').count()
    recent_students = Student.objects.order_by('-date_added')[:5]
    

    return render(request, 'dashboard.html', {
        'school_name': "Eldoret Poly CICT Group B",
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_attendance': total_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'recent_students': recent_students,
    })

# Students list, logins required to view students details
@login_required
def students(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})

# Teachers views
def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {'teachers': teachers})

# Attendance views
def attendance(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'attendance.html', {'attendance_records': attendance_records})


@login_required
@permission_required('core.add_student', raise_exception=True)
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student added successfully.")
                return redirect('students')
            except IntegrityError:
                form.add_error('admission_number', "A student with this admission number already exists.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})


@login_required
@permission_required('core.add_teacher')
def add_teacher(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        subject = request.POST['subject']
        email = request.POST['email']
        Teacher.objects.create(first_name=first_name, last_name=last_name, email=email, subject=subject)
        return redirect('teachers')
    return render(request, 'add_teacher.html')


@login_required
@permission_required('core.add_attendance')
def add_attendance(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST['student']
        status = request.POST['status']
        Attendance.objects.create(student_id=student_id, date=timezone.now().date(), status=status)
        return redirect('attendance')
    return render(request, 'add_attendance.html', {'students': students})

def student_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()
    if query:
        students = students.filter(Q(name_icontains=query) | Q(class_level_icontains=query))
        paginator = Paginator(students, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'students.html', {'page_obj': page_obj})
    

def teachers_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()
    if query:
        teachers = teachers.filter(Q(name_icontains=query) | Q(subject_icontains=query))
        paginator = Paginator(teachers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'teachers.html', {'page_obj': page_obj})


def attendance_list(request):
    
    attendance = Attendance.objects.all()
    
    return render(request, 'attendance.html', {'attendance': attendance})

 
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('students')

# Views to delete teachers
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect('teachers')


def delete_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.delete()
    return redirect('attendance')

def get_counts(request):
    data = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
    }
    return JsonResponse(data)


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if not remember:
                request.session.set_expiry(0)  # Expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            return redirect('dashboard')
        else:
            error = 'Invalid username or password'

    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists.'})
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        login(request, user)
        return redirect('dashboard') # redirect to dashboard after successful registration
    return render(request, 'register.html') 

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

# define unit here
from .models import Unit

def units_list(request):
    units = Unit.objects.all()
    return render(request, 'units_list.html', {'units': units})

def teacher_units(request):
    units = Unit.objects.filter(teacher=request.user)
    return render(request, 'teacher_list.html', {'units': units}) 



def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('unit_list')
    return render(request, 'delete.html', {'unit': unit})

def unit_list(request):
    units =Unit.objects.all()
    return render(request, 'units/unit_list.html', {'units': units})
def unit_add(request):
    form = UnitForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('unit_list')
    return render(request, 'units/unit_form.html', {'form': form})

def unit_edit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    form = UnitForm(request.POST or None, instance=unit)
    if form.is_valid():
        form.save()
        return redirect('unit_list')
    return render(request, 'unit_form.html', {'form': form})

def unit_delete(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    unit.delete()
    return redirect('unit_list')

# Attendance summary to summaries the attendance of each student

def attendance_summary(request):
    students = Student.objects.all()
    report_data = []

    total_present = 0
    total_absent = 0

    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='Present').count()
        absent = Attendance.objects.filter(student=student, status='Absent').count()
        total_present += present
        total_absent += absent
        
        percentage= 0
        if total > 0:
            percentage = round((present / total) * 100, 2) 
        report_data.append({
                'student': student.name,
                'present': present,
                'absent': absent,
                'percentage': percentage,

            })
        

    return render(request, 'attendance_summary.html', {
        'report_data': report_data,
        'total_present': total_present,
        'total_absent': total_absent,

    })

# class mission and vision
def static_mission_vision(request):
    return render(request, 'mission_vision.html')



        


    











