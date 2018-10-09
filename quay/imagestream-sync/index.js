
const http = require('http');
const https = require('https');
const fs = require('fs');
var express = require('express');
var cors = require('cors');
var app = express();
var bodyParser = require('body-parser');
var sync = require('./lib/sync');

const httpPort = process.env.HTTP_PORT || 8080;
const httpsPort = process.env.HTTPS_PORT || 8443;
const httpsSSLKey = process.env.HTTPS_SSL_KEY || '';
const httpsSSLCert = process.env.HTTPS_SSL_CERTIFICATE || '';


app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post('/', function (req, res) {

	if("docker_url" in req.body && "updated_tags" in req.body) {

		if(req.body.updated_tags instanceof Array) {

			sync.syncImageStreams(req.body, function(err, response){

				if(err) {
					res.status(500).send(err);
				}
				else {
					res.status(200).send(response);
				}
		
			});
		}
		else {
			console.info("Request does not contain a list of updated tags");
			res.status(204).send();
		}
	}
	else {
		res.status(400).send();
	}

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

