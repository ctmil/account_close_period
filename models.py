# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import numpy as np
from datetime import datetime,date,timedelta
from dateutil import relativedelta
import base64

class AccountMove(models.Model):
	_inherit = 'account.move'

	@api.multi
	def post(self):
		config_param = self.env['ir.config_parameter'].search([('key','=','LIMIT_ACCOUNT_POST_DAYS')])
		previous_date = None
		try:
			if config_param and int(config_param.value) > 0:
				days_parm = int(config_param.value)
				previous_date = date.today() - timedelta(days=days_parm)
		except:
			pass
		if previous_date:
			for am in self:
				if am.date < str(previous_date):
					raise ValidationError('No se puede realizar un movimiento contable tan en el pasado')	
		res = super(AccountMove, self).post()
		return res
