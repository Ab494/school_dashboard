from django.shortcuts import render, redirect
from .models import Student, Teacher, Attendance
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import UnitForm, StudentForm, TeacherForm
from .models import Unit
from django.db import IntegrityError
from django.utils import timezone
from .forms import AttendanceForm

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
        'school_name': "Eldoret Poly ICT Group B",
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
        form = StudentForm(request.POST, request.FILES)
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
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers')
    else:
        form = TeacherForm()
    return render(request, 'add_teacher.html', {'form': form})



@login_required
@permission_required('core.add_attendance')
def add_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        status = request.POST.get('status')
        date = request.POST.get('date') or timezone.now().date()
        if student_id and status:
            student = Student.objects.get(id=student_id)
            Attendance.objects.create(student=student, status=status, date=date)
            return redirect('attendance')
    students = Student.objects.all()
    today = timezone.now().date()
    today_records = Attendance.objects.filter(date=today).select_related('student')
    return render(request, 'add_attendance.html', {
        'students': students,
        'today_records': today_records,
    })
# Views for student list
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

# views to add units

@login_required
@permission_required("core.add_unit", raise_exception=True)
def unit_add(request):
    if request.method == 'POST':
        form = UnitForm(request.POST or None)
        if form.is_valid():
           form.save()
           messages.success(request, "Unit added successfully.")
           return redirect('unit_list')
    else:
        form = UnitForm()
    return render(request, 'add_unit.html', {'form': form})

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



        


    













# ── Health Check ──────────────────────────────────────
# Used by Render and UptimeRobot to verify the app is running
import time
from django.http import JsonResponse
from django.conf import settings
from django.db import connection

def health_check(request):
    start = time.time()

    # Check database
    db_status = 'healthy'
    db_response_time = None
    try:
        db_start = time.time()
        connection.ensure_connection()
        db_response_time = round((time.time() - db_start) * 1000, 2)
    except Exception:
        db_status = 'unhealthy'

    response_time = round((time.time() - start) * 1000, 2)

    data = {
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'environment': settings.DEBUG and 'development' or 'production',
        'services': {
            'database': {
                'status': db_status,
                'response_time_ms': db_response_time,
            }
        },
        'response_time_ms': response_time,
    }

    status_code = 200 if db_status == 'healthy' else 503
    return JsonResponse(data, status=status_code)


# ── Export Attendance PDF ─────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from django.http import HttpResponse
import datetime


def export_attendance_pdf(request):
    # Get data — same as attendance_summary view
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
        percentage = round((present / total) * 100, 2) if total > 0 else 0
        report_data.append({
            'student': student.name,
            'present': present,
            'absent': absent,
            'percentage': percentage,
        })

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ── Title ─────────────────────────────────────────
    title = Paragraph("<b>Eldoret National Poly ICT Group B</b>", styles['Title'])
    subtitle = Paragraph("Attendance Summary Report", styles['Heading2'])
    date_str = Paragraph(
        f"Generated on: {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}",
        styles['Normal']
    )
    elements.extend([title, subtitle, date_str, Spacer(1, 0.3 * inch)])

    # ── Summary Stats ─────────────────────────────────
    stats_data = [
        ['Total Students', 'Total Present', 'Total Absent'],
        [str(len(report_data)), str(total_present), str(total_absent)],
    ]
    stats_table = Table(stats_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, 1), 14),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, 1), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#2e7d32')),
        ('TEXTCOLOR', (2, 1), (2, 1), colors.HexColor('#c62828')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.extend([stats_table, Spacer(1, 0.3 * inch)])

    # ── Main Table ────────────────────────────────────
    table_data = [['#', 'Student Name', 'Days Present', 'Days Absent', 'Attendance %', 'Status']]

    for i, item in enumerate(report_data, 1):
        if item['percentage'] >= 75:
            status = 'Good'
        elif item['percentage'] >= 50:
            status = 'Average'
        elif item['percentage'] > 0:
            status = 'Poor'
        else:
            status = 'No Records'

        table_data.append([
            str(i),
            item['student'],
            str(item['present']),
            str(item['absent']),
            f"{item['percentage']}%",
            status,
        ])

    main_table = Table(table_data, colWidths=[0.4*inch, 2.2*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    main_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7ff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    # Color code the Status column
    for i, item in enumerate(report_data, 1):
        if item['percentage'] >= 75:
            main_table.setStyle(TableStyle([
                ('TEXTCOLOR', (5, i), (5, i), colors.HexColor('#2e7d32')),
                ('FONTNAME', (5, i), (5, i), 'Helvetica-Bold'),
            ]))
        elif item['percentage'] >= 50:
            main_table.setStyle(TableStyle([
                ('TEXTCOLOR', (5, i), (5, i), colors.HexColor('#f57f17')),
            ]))
        elif item['percentage'] > 0:
            main_table.setStyle(TableStyle([
                ('TEXTCOLOR', (5, i), (5, i), colors.HexColor('#c62828')),
            ]))

    elements.append(main_table)

    # ── Footer ────────────────────────────────────────
    elements.append(Spacer(1, 0.3 * inch))
    footer = Paragraph(
        "This report was generated automatically by the School Management System.",
        styles['Italic']
    )
    elements.append(footer)

    doc.build(elements)
    return response
