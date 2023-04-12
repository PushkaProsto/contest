from django.shortcuts import render
import subprocess
from django.contrib.auth.decorators import login_required

@login_required
def index(request): 
    if request.method == 'POST':        
        code = request.POST['interpreter']
        with open('1.py', 'w', encoding='utf8') as f:            
            f.write(code)
        k = subprocess.run('py 1.py', stdout=subprocess.PIPE)
        print(str(k))
        with open('1.txt', 'w', encoding='utf8') as f:
            f.write(str(k))
        context = {
            'posts': str(k).split("stdout=b'")[-1][:-6].split('\\r\\n')
        }
        print(context)
        
    
    else:
        context = {
            'posts': ''
        }
    return render(request, 'interpreter/index.html', context)