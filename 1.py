



import django
from core.models import Submission


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contest.settings')

django.setup()
for submission in Submission.objects.all():
    submission.slug = slugify(submission.task.name)
    submission.save()