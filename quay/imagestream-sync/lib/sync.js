const fs = require('fs');
const request = require('request');
const util = require('util');

const TOKEN_FILE = process.env.TOKEN_FILE || '/var/run/secrets/kubernetes.io/serviceaccount/token';
const CA_FILE = process.env.CA_FILE || '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt';
const AUTH_TOKEN = process.env.AUTH_TOKEN;
const MASTER_URL = process.env.MASTER_URL || 'https://kubernetes.default.svc:443'
const TLS_INSECURE = process.env.TLS_INSECURE
const NAMESPACE = process.env.NAMESPACE

var bearerToken
var caFile

if (TLS_INSECURE) {
	console.info("Enabling TLS Insecure Mode");
	process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
}

if (!NAMESPACE) {
	console.info("ImageStream Sync of All Namespaces Enabled");
}
else {
	console.info(util.format("ImageStream Sync for Namespace '%s' Enabled", NAMESPACE));
}


function getBearerToken() {

	if (bearerToken) {
		return bearerToken;
	}

	if (AUTH_TOKEN) {
		bearerToken = AUTH_TOKEN
		return bearerToken;
	}

	if (fs.existsSync(TOKEN_FILE)) {
		bearerToken = fs.readFileSync(TOKEN_FILE, "utf-8").trim();
		return bearerToken;
	}

}

function getCaCert() {

	if (caFile) {
		return caFile;
	}

	if (fs.existsSync(CA_FILE)) {
		caFile = fs.readFileSync(CA_FILE, "utf-8").trim();
		return caFile;
	}
}

function getMasterUrl() {
	return MASTER_URL;
}

function getImageStreamsUrl() {
	return util.format("%s/apis/image.openshift.io/v1%simagestreams", getMasterUrl(), (NAMESPACE == undefined) ? '/' : util.format("/namespaces/%s/", NAMESPACE));
}

function generateBaseRequestOptions() {
	var options = {}

	options['auth'] = { bearer: getBearerToken() };

	var caCert = getCaCert();

	if (caCert) {
		options['agentOptions'] = { ca: caCert };
	}

	return options;
}

async function syncImageStreams(requestBody, cb) {

	try {
		const imagestreams = await getImageStreams();
		Promise.all(generatePromises(requestBody.docker_url, requestBody.updated_tags, imagestreams)).then(function (results) {
			prepareResponse(cb, null, results);
		}).catch(function (promiseError) {
			prepareResponse(cb, promiseError, null);
		});

	}
	catch (err) {
		prepareResponse(cb, err, null);
	}


}

function generatePromises(docker_url, updated_tags, imageStreams) {
	var promises = []

	imageStreams.items.forEach(function (is) {
		if (is.spec.tags) {
			is.spec.tags.some(function (tag, tagIdx, _tagArr) {
				if (tag.from.kind == "DockerImage") {
					var imageTag = tag.from.name.split(':')
					var image = imageTag[0];
					var t = (imageTag.length == 2) ? imageTag[1] : 'latest';

					if (docker_url == image && updated_tags.includes(t)) {
						var imageStreamImport = generateImageStreamImport(is, tag);

						var updatePromise = new Promise((resolve, reject) => {

							var imageStreamImportOptions = Object.assign({
								uri: util.format("%s/apis/image.openshift.io/v1/namespaces/%s/imagestreamimports", getMasterUrl(), is.metadata.namespace),
								headers: {
									'Content-Type': 'application/json'
								},
								body: JSON.stringify(imageStreamImport)
							}, generateBaseRequestOptions());

							request.post(imageStreamImportOptions, function (importError, importResponse, importBody) {

								if (!importError && importResponse.statusCode == 201) {
									console.log(util.format("Imported ImageStream %s/%s:%s", is.metadata.namespace, is.metadata.name, t));
									resolve({success: {
										imageStream: is.metadata.name,
										tag: tag.name,
										namespace: is.metadata.namespace										
									}});
								}
								else {
									console.error(util.format("Error Importing ImageStream: %s/%s:%s", is.metadata.namespace, is.metadata.name, t));
									reject({error: {
										imageStream: is.metadata.name,
										tag: tag.name,
										namespace: is.metadata.namespace
									}});
								}
							});

						}).catch(function(err){
							return err;
						});

						promises.push(updatePromise);
					}

				}

			});
		}
	});

	return promises;
}


async function getImageStreams() {
	return new Promise((resolve, reject) => {

		var imageStreamRequestOptions = Object.assign({
			uri: getImageStreamsUrl()
		}, generateBaseRequestOptions());


		request(imageStreamRequestOptions, function (error, response, body) {
			if (!error && response.statusCode == 200) {
				resolve(JSON.parse(body));
			}
			else {
				console.error("Error Occurred Getting ImageStreams: " + error);
				reject({error: {
					message: "Error occurred while getting ImageStreams"
				}});
			}

		});

	});
}

function generateImageStreamImport(imageStream, tag) {

	tag["to"] = { name: tag.name};
	
	return {
		kind: "ImageStreamImport",
		apiVersion: "image.openshift.io/v1",
		metadata: {
			name: imageStream.metadata.name,
			namespace: imageStream.metadata.namespace,
			resourceVersion: imageStream.metadata.resourceVersion,
			creationTimestamp: null
		},
		spec: {
			import: true,
			images: [
				tag
			]
		},
		status: {}
	}
}

function prepareResponse(cb, errorMessage, successMessage) {
	if(errorMessage) {
		var response = {
			status: "error",
			message: errorMessage
		}

		cb(response, null);
	}
	else {
		var response = {
			status: "success",
			imageStreamSyncSuccess: [],
			imageStreamSyncFailure: []
		}

		successMessage.forEach(function (isResult) {

			if(isResult.hasOwnProperty("success")){
				response.imageStreamSyncSuccess.push(util.format("%s/%s:%s",isResult.success.namespace, isResult.success.imageStream, isResult.success.tag));
			}
			else if(isResult.hasOwnProperty("error")) {
				response.imageStreamSyncFailure.push(util.format("%s/%s:%s",isResult.error.namespace, isResult.error.imageStream, isResult.error.tag));
			}

		});

		cb(null, response);

	}
}

exports.syncImageStreams = syncImageStreams;