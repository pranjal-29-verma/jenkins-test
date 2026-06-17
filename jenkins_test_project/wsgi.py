import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jenkins_test_project.settings")
application = get_wsgi_application()
