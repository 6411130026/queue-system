# -*- coding: utf-8 -*-
#############################################################################
#
#    Hundred Solutions
#
#    Copyright (C) 2023-TODAY Hundred Solutions(<https://www.hundredsolutions.com/>)
#    Author: Arjun Baidya (arjun.b@hundredsolutions.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': 'Customer Queue',
    'version': '16.0.1.0.1',
    'summary': """Manage your customer by smart app""",
    'author': "Hundred Solutions",
    'maintainer': 'Hundred Solutions',
    'company': "Hundred Solutions",
    'website': 'https://www.hundredsolutions.com/',
    'category': 'Industries',
    'description': """
    Helps You To manage customer support.
    """,
    'depends': ['base', 'hr', 'contacts', 'mail', 'base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/demo_data.xml',
        # 'views/assets.xml',
        'views/token_create.xml',
        'views/counter_create_triage.xml',
        'views/hr_department_views.xml',
        'wizard/services.xml',
        'views/token_screen.xml',
        'wizard/token_screen.xml',
        'views/web_view.xml',
        'data/cron.xml',
        'views/waiting_screen_view.xml',
        'views/menu.xml',

    ],
    'images': ['static/description/banner.png'],
    'assets': {
        'web.assets_backend': [
            'customer_queue/static/src/js/waiting_screen.js',
            # 'customer_queue/static/src/css/waiting_screen.css',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
}
