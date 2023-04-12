from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Submission
from .forms import SubmissionForm, TaskForm
from django.contrib.auth.decorators import login_required
import chardet
from django.core.paginator import Paginator


@login_required
def task_create(request):
    if request.user.choice != '2':
        # Если пользователь не является преподавателем, перенаправляем на страницу с ошибкой.
        return render(request, 'core/error.html', {'message': 'Вы не имеете прав для создания задач.'})
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.prepod = request.user.username
            task = form.save()
            task.prepod = request.user.username
            task.save()
            return redirect('task_detail', slug=task.slug)

    return render(request, 'core/task_create.html', {'form': form})
def task_list(request):
    sort = request.GET.get('sort', 'name')  # получаем параметр сортировки из GET-запроса
    if sort == 'prepod':
        tasks = Task.objects.all().order_by('prepod')  # сортируем по полю "prepod"
    else:
        tasks = Task.objects.all().order_by('name')  # сортируем по умолчанию по полю "name"
    q = request.GET.get('q')
    if q:
        tasks = tasks.filter(name__icontains=q)

    paginator = Paginator(tasks,5)
    page_number = request.GET.get('page', 1)

    page = paginator.get_page(page_number)
    
    context = {
        'tasks': page.object_list,
        'page': page,
        'sort': sort, 
        'q': q}
    return render(request, 'core/task_list.html', context)


def author_tasks_view(request, prepod):
    tasks = Task.objects.filter(prepod=prepod).order_by('-created_at')
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'tasks': page,
        'page': page,
        'sort': request.GET.get('sort', ''),
        'q': request.GET.get('q', ''),
    }
    return render(request, 'core/task_list.html', context)

def task_detail(request, slug):
    task = get_object_or_404(Task, slug=slug)
    form = SubmissionForm()

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            submission = Submission.objects.create(
                task=task,
                code=code,
            )
            return redirect('submission_detail', pk=submission.pk)
    
    return render(request, 'core/task_detail.html', {'task': task, 'form': form})


@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    task = submission.task
    submission.prepod = submission.task.prepod
   
    input_data = (task.input.strip(), task.input1.strip(), task.input2.strip(),)
    expected_output = (task.output.strip(), task.output1.strip(), task.output2.strip(),)
                        
    passed = []   
    error = [] 
    output = []
    # Выполняем код студента в отдельном процессе с использованием входных данных
    # и получаем результат выполнения
    for i in range(3):
        if input_data[i] and expected_output[i]:
            
            from subprocess import Popen, PIPE
            process = Popen(['python', '-c', submission.code], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output_i, error_i = process.communicate(input=input_data[i].encode())
            try:
                encoding = chardet.detect(output_i)['encoding']
                output.append(output_i.decode(encoding).strip())
                passed.append(output_i.decode(encoding).strip() == expected_output[i])
            except:
                pass
            try:
                encoding = chardet.detect(error_i)['encoding']
                error.append(error_i.decode(encoding).strip())
            except:
                pass
            
            

            # Сравниваем полученный результат с ожидаемым результатом из задания
            
            
            
    if False in passed:
        passed = False
    for i in error:
        if i:
            error = i.strip()  
            break                 
    else:
        error = ''
    if error:
        submission.status = 'E'
    elif passed:
        submission.status = 'AC'
    else:
        submission.status = 'WA'
    if request.method == 'POST':
        submission.student = request.user.username
        submission.save()
        

    return render(request, 'core/submission_detail.html', {'submission': submission, 'output': ', '.join(output), 'error': error, 'passed': passed})




