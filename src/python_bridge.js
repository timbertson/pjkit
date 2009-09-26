var PYTHON = function(){
	var self = PYTHON;

	return {
		_last_cb_key: 1,
		_callbacks: new Array();

		call: function() {
			var args = Array.prototype.slice.call(arguments);
			var last_arg = args[args.length-1];
			var method = args.shift();

			var call = {
				method: method,
				args: args
			}
			if(typeof(last_arg) == 'function') {
				var callback = call.args.pop();
				call.respond_to = self._last_cb_key++;
				self._callbacks[call.respond_to] = args.pop();
			}

		},

		delegate: null,

		_send: function(obj) {
			document.title = "null";
			document.title = JSON.stringify(call);
		},

		_send_cb: function(id, val) {
			self._send({
				responding_to: id,
				value: val
			});
		},

		_recv_cb: function(id, str) {
			var obj = JSON.parse(str);
			self._callbacks[id](obj.value);
			delete self._callbacks[id];
		},

		_recv: function(str) {
			// expects obj to be a JSON-encoded string with fields
			// 'method', 'args' and optionally 'respond_to'
			var obj = JSON.parse(str);
			var delegate, func;
			var python_callback_key = null;
			if('respond_to' in obj) python_callback_key = obj.respond_to;
			if(self.delegate == null) {
				callee = null;
				func = eval(obj.method);
			} else {
				callee = delegate;
				func = delegate[obj.method];
			}
			var result = func.apply(delegate, obj.args);
			if(python_callback_key != null) {
				self._send_cb(python_callback_key, result);
			}
		}
	};
}();

