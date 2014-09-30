# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    tabs = db2.executesql('SELECT tabname from systables')

    return locals()

def get_members():
    members = db2(db2.member.name.startswith('LOP')).select(limitby=(20,30))
    return locals()

def show_ajax():
    if request.vars.id_no:
        redirect(URL('get_member', vars={'id_no':request.vars.id_no}))
    return locals()

def get_member():
    member_id = request.vars.id_no
    return locals()

def name_selector():
    
        
    if not request.vars.name: return ''
    
    pattern = request.vars.name.upper() + '%' 
    query = db2.member.name.like(pattern)
    if request.vars.first_name:
         pattern = request.vars.first_name.upper() + '%' 
         query &= db2.member.first_name.like(pattern)
            
    if request.vars.minst:
         pattern = request.vars.minst.upper() + '%' 
         query &= db2.member.minst.like(pattern)
     
    selected = [{'name':row.name, 'first_name':row.first_name, 'minst':row.minst, 'id_no':str(row.id_no)}for row in
               db2(query).select(orderby=db2.member.name | db2.member.first_name, limitby=(0,25))] #db2(db2.member.name.like(pattern)).select(orderby=db2.member.name, limitby=(0, 15))]
    return ''.join([DIV(k['name']+', '+k['first_name'] +', '+k['minst'],
                       _onclick="set_text('" +k['name']+"','"+k['first_name']+"','"+k['minst']+"','"+k['id_no']+"')",
                       _onmouseover="this.style.backgroundColor='yellow'",
                       _onmouseout="this.style.backgroundColor='white'"
                       ).xml() for k in selected])

def echo():
    return "$('#target').html(%s);" % repr(request.vars.name)

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
