# -*- coding: utf-8 -*-
# from odoo import http


# class Course(http.Controller):
#     @http.route('/course/course', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/course/course/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('course.listing', {
#             'root': '/course/course',
#             'objects': http.request.env['course.course'].search([]),
#         })

#     @http.route('/course/course/objects/<model("course.course"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('course.object', {
#             'object': obj
#         })
