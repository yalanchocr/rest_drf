import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toturial2.settings')
application = get_wsgi_application()

from myapp.import_products_data import handle_batch_import

zip_path = "./sample_data/sample1/sample1.zip"
msg = handle_batch_import("12", zip_path)
print(msg)
