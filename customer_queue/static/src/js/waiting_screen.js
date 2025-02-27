odoo.define('customer_queue.waiting_screen', function(require) {
    "use strict";

    var ajax = require('web.ajax');

    function updateQueue() {
        ajax.jsonRpc('/waiting_screen', 'call', {}).then(function(data) {
            $('#queue-list').html(data);
        });
    }

    setInterval(updateQueue, 1000); // รีเฟรชทุก 5 วินาที
});
