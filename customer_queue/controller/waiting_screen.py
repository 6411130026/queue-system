from odoo import http
from odoo.http import request

class WaitingScreen(http.Controller):

    @http.route('/waiting_screen', type='http', auth='public', website=True)
    def waiting_screen(self):
        queue_list = request.env['token.token'].sudo().search([('state', 'not in', ['done', 'cancel'])], order="name asc")
        return request.render('customer_queue.waiting_screen_template', {'queue_list': queue_list})
