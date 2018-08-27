
const request = require('request');
const urlModule = require('url');

const AnsibleTowerUrl = process.env['ANSIBLE_TOWER_URL'];
const AnsibleTowerTemplateId = process.env['ANSIBLE_TOWER_TEMPLATE_ID'];
const AnsibleTowerUsername = process.env['ANSIBLE_TOWER_USERNAME'] || '';
const AnsibleTowerPassword = process.env['ANSIBLE_TOWER_PASSWORD'] || '';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"


function getTemplateLaunchUri(){
	return '/api/v1/job_templates/' + AnsibleTowerTemplateId + '/launch/';
}

function getRequestUrl(server, uri){
	return 'https://' + server + uri;
}

function getAuth(){
	return 'Basic ' + new Buffer(AnsibleTowerUsername + ':' + AnsibleTowerPassword).toString('base64');
}


function generateReturnJson(message, url) {
	var returnjson = {
		message: message,
		url: ''
	};

	if (url) {
		returnjson['url'] = url;
	}

	return returnjson;
}


function sendResponse(cb, successMessage, errorMessage, url) {
	if (errorMessage) {
		console.log('ERROR: ' + errorMessage);
		returnjson = generateReturnJson(errorMessage, url);
		cb(returnjson, null);
	} else if (successMessage) {
		console.log('SUCCESS: ' + successMessage);
		returnjson = generateReturnJson(successMessage, url);
		cb(null, returnjson);
	} else {
		returnjson = generateReturnJson('Unknown Error');
		cb(returnjson, null);
	}
}


function processRequest(params, cb) {
	var uri = getTemplateLaunchUri();
	var request_url = getRequestUrl(AnsibleTowerUrl, uri);
	var auth = getAuth();

	var config_body = {
		"extra_vars" : {}
	};

	// Wrap the params in the `extra_vars` dictionary
	config_body['extra_vars'] = params;

	var options = {
		url: request_url,
		method: 'POST',
		headers: {
			'Content-type': 'application/json',
			'Authorization': auth
		},
		json: config_body
	};

	//	options_string = JSON.stringify(options, null, 4);
	//	console.log('calling options: ' + options_string);

	request(options, function (error, response) {
		//console.log('*********RESPONSE**********************');
		//console.log(response);
		//console.log('**********END RESPONSE*****************');
		if (!error && response.statusCode >= 200 && response.statusCode < 300) {
			sendResponse(
				cb,
				'Successful Launch with Ansible Tower job ID: ' + response.body.job,
				null,
				'https://' + AnsibleTowerUrl + '/#/jobs/' + response.body.job);

		}
		else {
			var errorMsg = 'Failed to launch Ansible Tower job. Please check your input and try again.';
			if (error) {
				errorMsg += ' (' + error + ')';
	 		}

			sendResponse(cb, null, errorMsg, null);
	  	}
	})
}


exports.processRequest = processRequest;
