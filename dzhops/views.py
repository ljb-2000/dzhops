# -*- coding: utf-8 -*-
#from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response
#from django.contrib import auth
#from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response,render,get_object_or_404  
from django.http import HttpResponse, HttpResponseRedirect  
from django.contrib.auth.models import User  
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required
import MySQLdb
from dzhops import settings
from common.saltapi import SaltAPI

#@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")

def index(request):
    # mysql
    conf = settings.DATABASES['default']
    serv_sql = '''SELECT * from `servstatus` order by id DESC limit 1'''
    proc_sql = '''SELECT * from `procstatus` order by id DESC limit 1'''
    mikey_sql = '''SELECT * from `minikeys` order by id DESC limit 1'''
    try:
        conn = MySQLdb.connect(
                host = conf['HOST'],
                user = conf['USER'],
                passwd = conf['PASSWORD'],
                db = conf['NAME'],
                port = conf['PORT'],
                charset='utf8')
        cursor = conn.cursor()
        n = cursor.execute(serv_sql)
        conn.commit()
        ret = {}

        for row in cursor.fetchall():
            ret['nowtime'] = row[1]
            ret['sysone'] = row[2]
            ret['sysfive'] = row[3]
            ret['sysfifteen'] = row[4]
            ret['cpuperc'] = row[5]
            ret['memtotal'] = row[6]
            ret['memused'] = row[7]
            ret['memperc'] = row[8]
            ret['disktotal'] = row[9]
            ret['diskused'] = row[10]
            ret['diskperc'] = row[11]

        cursor = conn.cursor()
        m = cursor.execute(proc_sql)
        conn.commit()
        for rowm in cursor.fetchall():
            ret['proctime'] = rowm[1]
            saltno = rowm[2]
            apino = rowm[3]
            myno = rowm[4]
            snmpno = rowm[5]

        cursor = conn.cursor()
        mk = cursor.execute(mikey_sql)
        conn.commit()
        for rowmk in cursor.fetchall():
            ret['mktime'] = rowmk[1]
            ret['num_miniall'] = rowmk[2]
            ret['num_miniup'] = rowmk[3]
            ret['num_minidown'] = rowmk[4]
            ret['num_mini'] = rowmk[5]
            ret['num_minipre'] = rowmk[6]
            ret['num_minirej'] = rowmk[7]

    except MySQLdb.Error,e:
        ret = {}
        ret['errno'] = e[0]
        ret['errinfo'] = e[1]
    
    if saltno == 0:
        ret['saltst'] = '正常'
    elif saltno == 1:
        ret['saltst'] = '异常'
    else:
        ret['saltst'] = 'UNKNOWN'

    if apino == 0:
        ret['apist'] = '正常'
    elif apino == 1:
        ret['apist'] = '异常'
    else:
        ret['apist'] = 'UNKNOWN'

    if myno == 0:
        ret['myst'] = '正常'
    elif myno == 1:
        ret['myst'] = '异常'
    else:
        ret['myst'] = 'UNKNOWN'
    
    if snmpno == 0:
        ret['snmpst'] = '正常'
    elif snmpno == 1:
        ret['snmpst'] = '异常'
    else:
        ret['snmpst'] = 'UNKNOWNN'



    return render_to_response('index.html', {'ret':ret})

def login(request):
    relt = 'hello\n\tWorld!'
    ret = {'zhaogb-201':'zhaogb-201','zhaogb-202':'zhaogb-202'}
    #ret = {'zhaogb-201':{'cont':'zhaogb-201','status': 'True'},'zhaogb-202':{'cont':'zhaogb-202','status': 'Fasle'},'zhaogb-203':{'cont':'zhaogb-203','status': 'Fasle'},'zhaogb-205':{'cont':'zhaogb-205','status': 'True'}}
    #ret = {u'file_|-info_so_1_|-/usr/lib64/libodbc.so.1_|-managed': {u'comment': u'File /usr/lib64/libodbc.so.1 is in the correct state', u'name': u'/usr/lib64/libodbc.so.1', u'start_time': u'09:33:32.468444', u'result': True, u'duration': 17.170000000000002, u'__run_num__': 2, u'changes': {}}, u'cmd_|-info_install_|-tar zxf /tmp/info.tar.gz -C /home/_|-run': {u'comment': u'Command "tar zxf /tmp/info.tar.gz -C /home/" run', u'name': u'tar zxf /tmp/info.tar.gz -C /home/', u'start_time': u'09:33:32.278982', u'result': True, u'duration': 188.48699999999999, u'__run_num__': 1, u'changes': {u'pid': 10564, u'retcode': 0, u'stderr': u'', u'stdout': u''}}, u'file_|-info_so_3_|-/usr/lib64/libltdl.so.3_|-managed': {u'comment': u'File /usr/lib64/libltdl.so.3 is in the correct state', u'name': u'/usr/lib64/libltdl.so.3', u'start_time': u'09:33:32.499477', u'result': True, u'duration': 6.6440000000000001, u'__run_num__': 4, u'changes': {}}, u'file_|-info_install_|-/tmp/info.tar.gz_|-managed': {u'comment': u'File /tmp/info.tar.gz is in the correct state', u'name': u'/tmp/info.tar.gz', u'start_time': u'09:33:31.743953', u'result': True, u'duration': 533.60500000000002, u'__run_num__': 0, u'changes': {}}, u'file_|-info_so_2_|-/usr/lib64/libodbc.so.2_|-managed': {u'comment': u'File /usr/lib64/libodbc.so.2 is in the correct state', u'name': u'/usr/lib64/libodbc.so.2', u'start_time': u'09:33:32.485824', u'result': True, u'duration': 13.279, u'__run_num__': 3, u'changes': {}}, u'file_|-info_service_|-/etc/init.d/infoservd_|-managed': {u'comment': u'File /etc/init.d/infoservd is in the correct state', u'name': u'/etc/init.d/infoservd', u'start_time': u'09:33:32.506618', u'result': True, u'duration': 8.1760000000000002, u'__run_num__': 5, u'changes': {}}}
    return render_to_response('login.html',{'ret': ret, 'relt': relt})
