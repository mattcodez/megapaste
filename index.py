import os
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class RenderMainPage(webapp.RequestHandler):
    def get(self):
        template_values = {
            'uploadLink': blobstore.create_upload_url('/new')
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
		
application = webapp.WSGIApplication([('/', RenderMainPage)
                                     ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()