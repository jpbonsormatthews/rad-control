//Environment Configuration
var config = {};
// replace the lines below...
config.IOT_BROKER_ENDPOINT      = "xxx";
config.IOT_BROKER_REGION        = "xxx";
config.IOT_THING_NAME           = "xxx";

//Loading AWS SDK libraries
var AWS = require('aws-sdk');
AWS.config.region = config.IOT_BROKER_REGION;

//Initializing client for IoT
var iotData = new AWS.IotData({endpoint: config.IOT_BROKER_ENDPOINT});

exports.handler = function (request, context) {
    log("DEGUG:", "Request",  JSON.stringify(request));

    if (request.directive.header.namespace === 'Alexa.Discovery') {
        log("DEGUG:", "Discover request",  "");
        handleDiscovery(request, context, "");
    } else if (request.directive.header.namespace === 'Alexa.ThermostatController') {
        log("DEBUG:", "ThermostatController Request", "");
        updateState(request, context);
    } else if (request.directive.header.namespace === 'Alexa' && request.directive.header.name === 'ReportState') {
        log("DEBUG:", "TemperatureSensor Request", "");
        sendStateReport(request, context);
    } else {
        log("ERROR:", "Unexpected Request", "");
        context.fail();
        return;
    }

    function handleDiscovery(request, context) {
        var payload = {
            "endpoints":
            [
                {
                    "endpointId": "kitchen-stat",
                    "manufacturerName": "JBM",
                    "friendlyName": "Kitchen",
                    "description": "Kitchen",
                    "displayCategories": ["THERMOSTAT"],
                    "cookie": {
                    },
                    "capabilities":
                    [
                        {
                            "type": "AlexaInterface",
                            "interface": "Alexa.ThermostatController",
                            "version": "3",
                            "properties": {
                                "supported": [
                                    { "name": "targetSetpoint" },
                                    { "name": "thermostatMode" }
                                ],
                                "proactivelyReported": false,
                                "retrievable": true
                            }
                        },
                        {
                            "type": "AlexaInterface",
                            "interface": "Alexa.TemperatureSensor",
                            "version": "3",
                            "properties": {
                                "supported": [
                                    { "name": "temperature" }
                                ],
                                "proactivelyReported": false,
                                "retrievable": true
                            }
                        }
                    ]
                }
            ]
        };
        var header = request.directive.header;
        header.name = "Discover.Response";
        log("DEBUG", "Discovery Response: ", JSON.stringify({ header: header, payload: payload }));
        context.succeed({ event: { header: header, payload: payload } });
    }

    function sendStateReport(request, context) {
        var params = {
            "thingName" : config.IOT_THING_NAME
        };
        iotData.getThingShadow(params, function (err, data) {
            if (err) {
                console.log("ERROR: failed to read shadow for report");
                console.log(err, err.stack);
                context.fail();
            } else {
                console.log("DEBUG: read shadow for report");
                console.log(data);
                var dataJ = JSON.parse(data.payload);

                var resp = {
                    "context": {
                        "properties": [
                            {
                                "namespace": "Alexa.EndpointHealth",
                                "name": "connectivity",
                                "value": {
                                    "value": "OK"
                                },
                                "timeOfSample": "2018-01-06T20:44:30.45Z",
                                "uncertaintyInMilliseconds": 200
                            },
                            {
                                "name": "targetSetpoint",
                                "namespace": "Alexa.ThermostatController",
                                "value": {
                                    "scale": "CELSIUS",
                                    "value": dataJ.state.desired.kitchen
                                },
                                "timeOfSample": "2018-01-06T20:44:30.45Z",
                                "uncertaintyInMilliseconds": 200
                            },
                            {
                                "name": "thermostatMode",
                                "namespace": "Alexa.ThermostatController",
                                "value": "AUTO",
                                "timeOfSample": "2018-01-06T20:44:30.45Z",
                                "uncertaintyInMilliseconds": 200
                            },
                            {
                                "name": "temperature",
                                "namespace": "Alexa.TemperatureSensor",
                                "value": {
                                    "scale": "CELSIUS",
                                    "value":  dataJ.state.reported.kitchen
                                },
                                "timeOfSample": "2018-01-06T20:44:30.45Z",
                                "uncertaintyInMilliseconds": 200
                            }
                        ]
                    },
                    "event": {
                        "header": {
                            "namespace": "Alexa",
                            "name": "StateReport",
                            "payloadVersion": "3",
                            "messageId": "78500685-6c9c-46c0-9ebc-ff84ec3c086c",
                            "correlationToken": request.directive.header.correlationToken
                        },
                        "endpoint": {
                            "scope": {
                                "type": "BearerToken",
                                "token": request.directive.endpoint.scope.token
                            },
                            "endpointId": "kitchen-stat"
                        },
                        "payload": {}
                    }
                };
                log("DEBUG", "State Report Response: ", JSON.stringify(resp));
                context.succeed(resp);
            }
        });
    }

    function updateState(request, context) {
        var params = {
            "thingName" : config.IOT_THING_NAME
        };
        iotData.getThingShadow(params, function (err, data) {
            if (err) {
                console.log("ERROR: failed to read shadow for setting");
                console.log(err, err.stack);
                context.fail();
            } else {
                console.log("DEBUG: read shadow for setting");
                console.log(data);
                var dataJ = JSON.parse(data.payload);

                var payloadObj={ "state":
                                 { "desired":
                                   {"kitchen":request.directive.payload.targetSetpoint.value}
                                 }
                               };
                var paramsUpdate = {
                    "thingName" : config.IOT_THING_NAME,
                    "payload" : JSON.stringify(payloadObj)
                };
                iotData.updateThingShadow(paramsUpdate, function(err, dataUp) {
                    if (err){
                        console.log("ERROR: failed to update shadow for setting");
                        console.log(err, err.stack);
                        context.fail();
                    } else {
                        console.log("DEBUG: read shadow for report");
                        console.log(dataUp);

                        var resp = {
                            "context": {
                                "properties": [
                                    {
                                        "namespace": "Alexa.EndpointHealth",
                                        "name": "connectivity",
                                        "value": {
                                            "value": "OK"
                                        },
                                        "timeOfSample": "2018-01-06T20:44:30.45Z",
                                        "uncertaintyInMilliseconds": 200
                                    },
                                    {
                                        "name": "targetSetpoint",
                                        "namespace": "Alexa.ThermostatController",
                                        "value": {
                                            "scale": "CELSIUS",
                                            "value": request.directive.payload.targetSetpoint.value
                                        },
                                        "timeOfSample": "2018-01-06T20:44:30.45Z",
                                        "uncertaintyInMilliseconds": 200
                                    },
                                    {
                                        "name": "thermostatMode",
                                        "namespace": "Alexa.ThermostatController",
                                        "value": "AUTO",
                                        "timeOfSample": "2018-01-06T20:44:30.45Z",
                                        "uncertaintyInMilliseconds": 200
                                    },
                                    {
                                        "name": "temperature",
                                        "namespace": "Alexa.TemperatureSensor",
                                        "value": {
                                            "scale": "CELSIUS",
                                            "value": dataJ.state.reported.kitchen
                                        },
                                        "timeOfSample": "2018-01-06T20:44:30.45Z",
                                        "uncertaintyInMilliseconds": 200
                                    }
                                ]
                            },
                            "event": {
                                "header": {
                                    "namespace": "Alexa",
                                    "name": "Response",
                                    "payloadVersion": "3",
                                    "messageId": "78500685-6c9c-46c0-9ebc-ff84ec3c086c",
                                    "correlationToken": request.directive.header.correlationToken
                                },
                                "endpoint": {
                                    "scope": {
                                        "type": "BearerToken",
                                        "token": request.directive.endpoint.scope.token
                                    },
                                    "endpointId": "kitchen-stat"
                                },
                                "payload": {}
                            }
                        };
                        log("DEBUG", "Setting Report Response: ", JSON.stringify(resp));
                        context.succeed(resp);
                    }
                });
            }
        });
    }

    function log(message, message1, message2) {
        console.log(message + message1 + message2);
    }
};
