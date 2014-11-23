import sae
from doctor import wsgi

application = sae.create_wsgi_app(wsgi.application)


