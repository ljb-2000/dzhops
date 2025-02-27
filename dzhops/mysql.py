# -*- coding: utf-8 -*-
import MySQLdb
import json
import settings

class db_operate:
    def mysql_command(self,conn,sql_cmd):
        try:
            ret = []
            conn=MySQLdb.connect(host=conn['default']['HOST'],user=conn['default']['USER'],passwd=conn['default']['PASSWORD'],db=conn['default']['NAME'],port=conn['default']['PORT'],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
        except MySQLdb.Error,e:
            ret.append(e)

        return ret

    def select_table(self,conn,sql_cmd,parmas):
        '''
        out(type:dict)  {'host1':{'dict_content'},'host2':{'dict_content'},...}
        '''
        try:
            unret = {}
            ret = {}
            conn=MySQLdb.connect(host=conn['default']['HOST'],user=conn['default']['USER'],passwd=conn['default']['PASSWORD'],db=conn['default']['NAME'],port=conn['default']['PORT'],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd,parmas)
            for row in cursor.fetchall():
                val = json.loads(row[1])
                unret[row[0]] = val
                ret.update(unret)
        except MySQLdb.Error,e:
            unret['MysqlErro'] = e
            ret.undate(unret)

        return ret
