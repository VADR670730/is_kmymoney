# -*- coding: utf-8 -*-

from openerp import tools
from openerp import models,fields,api
from openerp.tools.translate import _


class SoldeParAnReport(models.Model):
    _name = "kmn.solde.par.an.report"
    _description = "Solde par an et par compte"
    _auto = False
    _rec_name = 'compte'

    compte = fields.Char(u'Compte')
    annee  = fields.Date(u'Année')
    solde  = fields.Float(u'Solde', digits=(1, 0), readonly=True)


    def init(self):
        cr , uid, context = self.env.args
        tools.drop_view_if_exists(cr, 'kmn_an')
        cr.execute("""CREATE or REPLACE VIEW kmn_an as (
            select distinct (to_char(post_date,'YYYY-12-31'))::date  annee 
            from kmn_account_move 
            where post_date>='2008-01-01' 
            order by annee
        )""")

        tools.drop_view_if_exists(cr, 'kmn_solde_par_an_report')

        cr.execute("""CREATE or REPLACE VIEW kmn_solde_par_an_report as (
            select 
                a.id,
                a.name as compte, 
                annee ,
                (coalesce((select sum(value) from kmn_account_move where account2_id=a.id and post_date<=annee),0) -
                 coalesce((select sum(value) from kmn_account_move where account1_id=a.id and post_date<=annee),0)) as solde
            from kmn_accounts a, kmn_an
            where a.institution_id is not null and active=true 
            order by a.name, annee
        )""")


#                round((
#                    (select sum(value) from kmn_account_move where account2_id=a.id and post_date<=annee)-
#                    (select sum(value) from kmn_account_move where account1_id=a.id and post_date<=annee))::numeric,2) as solde




