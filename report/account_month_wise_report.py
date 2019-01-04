# -*- coding: utf-8 -*-
# #############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import tools
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv



class account_month_wise_report(osv.osv):
    _name = "account.month.wise.report"
    _description = "Account month wise"
    _auto = False
    _rec_name = 'acc_name'

    _columns = {
        #'month_name': fields.char('Month Name'),
        'post_date': fields.date('Date'),
        'acc_name': fields.char('Account'),
        'bal_value': fields.float('Balance', digits=(1, 3), readonly=True),
    }
    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        cr.execute("truncate table account_month_table RESTART IDENTITY;")
        cr.execute("""
            insert into account_month_table (post_date,acc_name,value) 
             select myear as post_date,acc_name,sum(credit)-sum(debit) as bal_value
             from (
             select cast(to_char(post_date,'MM-01-YYYY') as date) as myear,sum(value) as debit,0 as credit,kmn_accounts.name as acc_name
             from kmn_account_move
             inner join kmn_accounts on kmn_accounts.id=kmn_account_move.account1_id             
             group by to_char(post_date,'MM-01-YYYY'),kmn_accounts.name
             union all
             select cast(to_char(post_date,'MM-01-YYYY') as date) as myear,0 as debit,sum(value) as credit,kmn_accounts.name as acc_name
             from kmn_account_move
             inner join kmn_accounts on kmn_accounts.id=kmn_account_move.account2_id
             group by to_char(post_date,'MM-01-YYYY'),kmn_accounts.name
             ) a group by myear,acc_name order by myear,row_number() over(order by myear desc)
        """)
         
        #cr.execute("insert into account_month_table (acc_name,value,post_date) values ('ACC1',0,'2015-03-01')")
        cr.execute("select distinct post_date from account_month_table order by post_date")
        year_data = cr.fetchall()       
         
         
        cr.execute("select distinct acc_name from account_month_table order by acc_name")
        data = cr.fetchall()
         
        for acc_name in data:
             
            for year in year_data:
                cr.execute("select count(*) from account_month_table where acc_name=%s and post_date=%s",(acc_name,year))
                is_value = cr.fetchone()[0]
                if is_value == 0:
                    cr.execute("insert into account_month_table (acc_name,value,post_date) values ('"+acc_name[0]+"',0,'"+year[0]+"')")
             
            cr.execute("select id,value from account_month_table where acc_name=%s order by post_date",(acc_name))
            update_data = cr.fetchall()
            i = 1
            bal = 0
            for rec in update_data:
                bal += rec[1]
                if i != 1:
                    cr.execute("update account_month_table set value=%s where id=%s"%(bal,rec[0]))
                i += 1
                            
        return super(account_month_wise_report, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'account_month_wise_report')
        cr.execute("""CREATE or REPLACE VIEW account_month_wise_report as (
        select id,post_date,value as bal_value,acc_name
        from account_month_table        
        )""")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: