"""
WSGI config for toturial2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toturial2.settings')

application = get_wsgi_application()




from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
#
# snippet = Snippet(code='foo = "bar"\n')
# snippet.save()
#
# snippet = Snippet(code='print("hello, world")\n')
# snippet.save()
#
# serializer = SnippetSerializer(snippet)
# print(type(serializer.data))
#
# content = JSONRenderer().render(serializer.data)
# print(type(content))
#
# import io
#
# stream = io.BytesIO(content)
# data = JSONParser().parse(stream)
#
# serializer = SnippetSerializer(data=data)
# serializer.is_valid()
# # True
# print(serializer.validated_data)
# # OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
# serializer.save()
# # <Snippet: Snippet object>
#
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
print(type(serializer.data), serializer.data)


from snippets.serializers import SnippetSerializer
serializer = SnippetSerializer()
print(repr(serializer))