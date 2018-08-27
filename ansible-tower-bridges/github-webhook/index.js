
const http = require('http');
const https = require('https');
const fs = require('fs');

const httpPort = process.env.HTTP_PORT || 8080;
const httpsPort = process.env.HTTPS_PORT || 8443;
const httpsSSLKey = process.env.HTTPS_SSL_KEY || '';
const httpsSSLCert = process.env.HTTPS_SSL_CERTIFICATE || '';

var express = require('express');
var cors = require('cors');
var app = express();
var bodyParser = require('body-parser');
var bridge = require('./lib/bridge');

app.use(cors());
app.use(bodyParser());

app.post('/', function (request, res) {
	bridge.processRequest(request.body, function(err, response) {
		if (err){
			// TODO: make the return status code be more specific per the error
			// - i.e.: not use "400 Bad Request" for all of it
			res.status(400).send(err);
		} else {
			res.send(response);
		}
	});
});

if (httpsSSLCert.trim() && httpsSSLKey.trim()) { // Secure
	const options = {
		  key: fs.readFileSync(httpsSSLKey),
		  cert: fs.readFileSync(httpsSSLCert)
	};

	https.createServer(options, app).listen(httpsPort, function () {
		console.log('Listening on https://localhost:' + httpsPort);
	});
}
else { 	// non-Secure
	http.createServer(app).listen(httpPort, function() {
		console.log('Listening on UNSECURE http://localhost:' + httpPort);
	});
}
