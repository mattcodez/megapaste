import os
import cgi
import mpDB

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from mpDB import *

class RenderRecentPosts(webapp.RequestHandler):
    def get(self):
		pastes = Paste.all().filter('private != ', True).order('private').order('-date')
		template_values = {
			'pastes':	pastes
		}

		path = os.path.join(os.path.dirname(__file__), 'recent.html')
		self.response.out.write(template.render(path, template_values))
		
application = webapp.WSGIApplication([('/recent', RenderRecentPosts)
                                     ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()