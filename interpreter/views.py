from django.shortcuts import render
from subprocess import Popen, PIPE
from django.contrib.auth.decorators import login_required
import chardet

@login_required
def index(request): 
    if request.method == 'POST':        
        code = request.POST['interpreter']
        process = Popen(['python', '-c', code], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate(input='test'.encode())
        
        context = {'1':'1'}
        
        try:
            encoding = chardet.detect(output)['encoding']
            contest['posts'] = output.decode(encoding).strip()            
        except:
            pass
        try:
            encoding = chardet.detect(error)['encoding']
            contest['error'] = error.decode(encoding).strip()
        except:
            pass   
    
    else:
        context = {
            'posts': '',
            'error': '',
        }
    return render(request, 'interpreter/index.html', context)
