#!/usr/bin/env python

import datetime
import markdown
import os
import random
import re
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

def slugify(inStr):
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
    for a in removelist:
        aslug = re.sub(r'\b'+a+r'\b','',inStr)
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return aslug

class Note(db.Model):
  """Represents a single note.
  """
  note_title = db.TextProperty(required=True)
  note_text = db.TextProperty(required=True)
  slug = db.StringProperty()
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
      notes = db.GqlQuery("SELECT * from Note ORDER BY created DESC");
      self.generate('index.html', {
          'notes': notes,
      })

  def post(self):
      note_title = self.request.get('note_title')
      note_text =  self.request.get('note_text')
      slug = slugify(note_title) 
      if (note_text and note_title):
          record = Note(note_title=note_title,note_text=note_text,slug=slug);
          record.put()
      self.redirect('/')

class NoteEditPage(BaseRequestHandler):
  @login_required
  def get(self,key=0):
      notes = db.GqlQuery("SELECT * from Note ORDER BY created DESC");
      note = Note.get(key)
      self.generate('edit.html', {
          'note_title': note.note_title,
          'note_text': note.note_text,
          'note_key': key,
          'notes' : notes,
      })

  def post(self,key=0):
      note = Note.get(key)
      note.note_title = self.request.get('note_title')
      note.note_text =  self.request.get('note_text')
      note.slug = slugify(note.note_title) 
      note.put()
      self.redirect('/note/'+note.slug)

class NoteTextPage(BaseRequestHandler):
  def get(self,slug=0):
      q = Note.all()
      q.filter('slug =',slug) 
      md = markdown.Markdown()
      res = q.fetch(1)
      for note in res:
          self.generate('note_text.html', {
              'note_title': note.note_title,
              'note_text': md.convert(note.note_text),
          })

class NotePage(BaseRequestHandler):
  def get(self,slug=0):
      notes = db.GqlQuery("SELECT * from Note ORDER BY created DESC");
      q = Note.all()
      q.filter('slug =',slug) 
      md = markdown.Markdown()
      res = q.fetch(1)
      for note in res:
          self.generate('note.html', {
              'note_title': note.note_title,
              'note_text': md.convert(note.note_text),
              'notes': notes,
          })

def main():
  application = webapp.WSGIApplication([
    ('/', NotesPage),
    ('/notes', NotesPage),
    ('/edit/(.*)', NoteEditPage),
    ('/text/(.*)', NoteTextPage),
    ('/note/(.*)', NotePage),
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
