# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


# @auth.requires_login()
# def addItem():
#     item = db(db.item.id==request.args(0)).select().first()
#     db.comment.image_id.default = image.id
#     form = SQLFORM(db.comment)
#     if form.process().accepted:
#         response.flash = 'your comment is posted'
#     comments = db(db.comment.image_id==image.id).select()
#     return dict(image=image, comments=comments, form=form)

def user():
    return dict(form=auth())


@auth.requires_login()
def additem():
    form = SQLFORM(db.item)
    if form.process().accepted:
        response.flash = 'your item is added'
    return dict(form=form)


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # response.flash = T("Hello World")
    # return dict(message=T('Welcome to web2py!'))
    response.flash = 'This is HW2, Please use tom@gmail.com or  jm.miller@gmail.com or g_samy@gmail.com or green1988@outlook.com to login, Add/ Edit button will be shown on top left,   all password is: "123456" To see this message again, please refresh page'
    items = db().select(db.item.ALL, orderby=db.item.title,limitby=(0, 10))
    return dict(items=items)

@auth.requires_login()
def edit():
    item = db.item[request.args(0)]
    form = SQLFORM(db.item, item,labels = {'title' : "Title", 'seller' : "Seller"},

    showid = False,
    deletable = True,
    submit_button = 'update your item'
    )

    if form.process(keepvalues=True).accepted:
       response.flash = 'Update accepted'
    elif form.errors:
       response.flash = 'Please complete your item'
    else:
       response.flash = 'Please edit your item'
    items = db(db.item.valid==True).select()

    return dict(form=form)

@auth.requires_login()
def edit_item():
    items = db(db.item.user_id == auth.user_id).select()
    response.flash = 'Hello' + ' ' + db.auth_user[auth.user_id].first_name + ', Please Choose the item you want to edit'
    return dict(items=items)


def onsale():
    items = db(db.item.valid==True).select()
    return dict(items=items)


def download():
    return response.download(request, db)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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
