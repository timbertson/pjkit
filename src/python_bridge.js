var PYTHON = function(){
	return {
		_last_cb_key: 1,
		_callbacks: new Array(),

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
				call.respond_to = PYTHON._last_cb_key++;
				PYTHON._callbacks[call.respond_to] = args.pop();
			}
			PYTHON._send(call);

		},

		delegate: null,

		_send: function(obj) {
			document.title = "null";
			document.title = JSON.stringify(obj);
		},

		_send_cb: function(id, val) {
			PYTHON._send({
				responding_to: id,
				value: val
			});
		},

		_recv_cb: function(id, str) {
			alert("got cb: " + str);
			var obj = JSON.parse(str);
			PYTHON._callbacks[id](obj.value);
			delete PYTHON._callbacks[id];
		},

		_recv: function(str) {
			// expects obj to be a JSON-encoded string with fields
			// 'method', 'args' and optionally 'respond_to'
			var obj = JSON.parse(str);
			var delegate, func;
			var python_callback_key = null;
			if('respond_to' in obj) python_callback_key = obj.respond_to;
			if(PYTHON.delegate == null) {
				callee = null;
				func = eval(obj.method);
			} else {
				callee = delegate;
				func = delegate[obj.method];
			}
			var result = func.apply(delegate, obj.args);
			if(python_callback_key != null) {
				PYTHON._send_cb(python_callback_key, result);
			}
		}
	};
}();

