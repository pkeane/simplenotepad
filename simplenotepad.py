#!/usr/bin/env python

import datetime
import os
import random
import string
import sys
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class Note(db.Model):
  """Represents a single note.
  """
  note_title = db.TextProperty(required=True)
  note_text = db.TextProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)


class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
      'user': users.GetCurrentUser(),
      'login_url': users.CreateLoginURL(self.request.uri),
      'logout_url': users.CreateLogoutURL('http://' + self.request.host + '/'),
      'debug': self.request.get('deb'),
      'application_name': 'Simple Notepad',
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))


class NotesPage(BaseRequestHandler):
  """Lists the notes """

  @login_required
  def get(self,id=0):
    self.generate('index.html', {
      'id': id,
    })

  def post(self,id=0):
    self.generate('index.html', {
      'id': id,
    })


class NotePage(BaseRequestHandler):
  @login_required
  def get(self,id=0):
    self.generate('index.html', {
      'id': id,
    })

def main():
  application = webapp.WSGIApplication([
    ('/', NotesPage),
    ('/post', NotesPage),
    ('/note', NotePage),
    (r'/note/(.*)', NotePage),
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
