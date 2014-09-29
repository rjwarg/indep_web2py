# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from datetime import date

def index():
    rows = db(db.case_master).select()
    return locals()

def edit_case():
    testing = "testing"
    case_number = request.args(1)
    if case_number == 'new':
        case_number = new_case_number()
        form = SQLFORM(db.case_master)
        form.vars.case_number = case_number
        form.vars.member_id = 1001
        
    else:
        case = db.case_master(request.args(0))
        form = SQLFORM(db.case_master, case)
        
    if form.process(session=None, formname='indep').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill in the form'
        
    return locals()

def other():
    # note: from hot italian
    message = 'Welcome %s , your birth date is % s' % (request.vars.your_name, request.vars.birth_date)
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def new_case_number():
    
 
    suffix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    date_part = date.today().strftime("%Y%m%d")
    # howmany cases start with this date?
    count = db(db.case_master.case_number.like(date_part +'%')).count()
    return date_part + suffix[count:count+1]
