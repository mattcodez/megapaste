import cgi
import mpDB

from string import Template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from mpDB import *

class Listings(webapp.RequestHandler):
  def get(self):
	self.response.out.write('<html><head>')

	paste = Paste.get(db.Key(self.request.get('id')))

	self.response.out.write('<title>%s</title></head><body>' % cgi.escape(paste.title))
	self.response.out.write('<i>%s</i>' % (paste.date))
	
	images = Image.all().filter('paste = ', paste.key())
	body = cgi.escape(paste.content)
	self.response.out.write('<p># of images: %s</p>' % images.count())
	for img in images:
		if img.shrunk:
			body = body.replace('[img' + str(img.localID) + ']', ('<a target="_blank" href="imgview?imgKey=%s"><img src="imgview?shrinkKey=%s" /></a>' % (img.img.key(), img.key())), 20)
		else:
			body = body.replace('[img' + str(img.localID) + ']', ('<img src="imgview?imgKey=%s" />' % img.img.key()), 20)
	
	self.response.out.write('<blockquote>%s</blockquote>' % body)
	
	self.response.out.write('</body></html>')

application = webapp.WSGIApplication(
                                     [('/view', Listings)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()