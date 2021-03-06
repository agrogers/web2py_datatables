# -*- coding: utf-8 -*-
print('================================================ APPLICATION STARTED ================================================')

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from gluon.custom_import import track_changes; track_changes(True)  # Imports changes to my custom modules
from gluon import current  # This is needed to make db available in modules that I import. See https://stackoverflow.com/questions/11959719/web2py-db-is-not-defined

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'],
             #lazy_tables=True
             )
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

current.db = db  # This is needed to make db available in modules that I import. See note above.

#----------------------------------------------------------------------
# Run tidy up SQL commands here
#----------------------------------------------------------------------
#db.auth_user.truncate
#db.executesql('DELETE FROM auth_user')

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.settings.password_min_length = 1

# -------------------------------------------------------------------------
# Custom auth_user table. I want the last_name to be optional but i cant see
# a way to do that without  creating my own table.
# This must be done before the auth.define_tables

#http://www.lingoes.net/en/translator/langcode.htm has a list of languages
# 'Language' is a KEY word so i cant name the table that :-(
db.define_table(
    'Languages',
    Field('Code', required=True),
    Field('LongName', required=True),
    Field('ShortName',required=False),
    format = '%(Code)s (%(LongName)s)',
#     migrate = False
)

db.define_table(
    auth.settings.table_user_name,
    Field('DisplayName', length=128, default='', label='Name'),
    Field('username', label='Username'),  # , unique=True, required=True),
    Field('first_name', length=128, default='', label='First Name'),
    Field('last_name', length=128, default='', label='Last Name'),
    Field('email', length=128, default='', unique=True),  # required
    Field('password', 'password', length=512,             # required
          readable=False, label='Password'),
    Field('PreferredLanguageID',db.Languages, label='Preferred Language', default=session.OrganisationLanguage),
    Field('DOB',type='date', label='DOB'),
    Field('address'),
    Field('city'),
    Field('zip'),
    Field('phone'),
    Field('registration_key', length=512,                 # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,               # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                  # required
          writable=False, readable=False, default=''),
    format=lambda r: (r.DisplayName)
    #format=lambda r: (r.last_name.upper() + ', ' + r.first_name) if (r.last_name) else r.first_name
)


custom_auth_table = db[auth.settings.table_user_name]  # get the custom_auth_table
custom_auth_table.DisplayName.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
#custom_auth_table.last_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
#custom_auth_table.password.requires = [IS_STRONG(), CRYPT()]
custom_auth_table.password.requires = [CRYPT()]
custom_auth_table.email.requires = [
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, custom_auth_table.email)]
custom_auth_table.username.requires = IS_NOT_IN_DB(db, custom_auth_table.username)
custom_auth_table._Icon = '/smartdeck/static/img/icons/set1/svg/users.svg'

# See http://web2py.com/books/default/chapter/29/09/access-control#Auth-Settings-and-messages for more info
auth.settings.table_user = custom_auth_table  # tell auth to use custom_auth_table
auth.settings.registration_requires_verification = False
auth.settings.login_after_registration = True

auth.define_tables(username=False, signature=False)

db._common_fields.append(auth.signature)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
