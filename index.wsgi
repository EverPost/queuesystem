import sae
from queuesystem import wsgi

application = sae.create_wsgi_app(wsgi.application)