from flask import Flask, redirect, url_for, render_template, request, render_template_string
import graphene
from graphene import ObjectType, String, Schema, List
import xmltodict, json
import requests
from datetime import datetime, timedelta

app = Flask(__name__)


class Query(ObjectType):
    rate = graphene.String(items=String(default_value="ERROR"))
    label = graphene.String(
        ServiceName=String(default_value="ERROR"),
        LabelCost=String(default_value="ERROR"),
        LabelPdf=String(default_value="ERROR")        
        )
    void = graphene.String(
        Status=String(default_value="ERROR"),
        Message=String(default_value="ERROR"),     
        )
    def resolve_rate(root, info, items):
        return items
    def resolve_label(root, info, LabelCost, ServiceName, LabelPdf):
        return f'Your service name: {ServiceName}, the cost: ${LabelCost}, and the pdf: {LabelPdf}'
    def resolve_void(root, info, Status, Message):
        return f'STATUS: {Status}, Message: {Message}'


schema = graphene.Schema(query=Query)
@app.route("/rates", methods=['POST'])

def rates():
    url = 'https://wsbeta.fedex.com:443/web-services'
    headers = {
        'Content-Type': 'text/xml'
        }
    time = datetime.utcnow() + timedelta(hours=1)
    futureTime = time.isoformat()
    post_data = render_template('RateService_getRates_Request.xml', key='4UK71Z09zHJvRHux',
        password='DY6sq7EGkRcraIIC6DoefnvQc',
        account_number=510087100,
        meter_number=119242929,
        time = futureTime)
    req = requests.post(url, data=post_data, headers=headers)
    obj = xmltodict.parse(req.content)
    ServiceDescription = obj["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["RateReply"]["RateReplyDetails"]
    service_list = []
    for service in ServiceDescription:
        response_dict = {
            'Service Name': str(service["ServiceDescription"]['Description']),
            'Service Code': str(service["ServiceDescription"]['Code']),
            'Cost': (service["RatedShipmentDetails"][1]['ShipmentRateDetail']['TotalNetChargeWithDutiesAndTaxes']['Amount']),
            'Transit Time': 'None'
        }
        service_list.append(response_dict)
    

    query = '{{ rate(items: "{service_list}") }}'.format(
        service_list=service_list)
    result = schema.execute(query)
    return result.data['rate']

schema = graphene.Schema(query=Query)
@app.route("/label", methods=['POST'])

def label():
    url = 'https://wsbeta.fedex.com:443/web-services'
    headers = {
        'Content-Type': 'text/xml'
        }
    post_data = render_template('Fedex_Ground_home_delivery_V26_Ext_Request.xml', key='4UK71Z09zHJvRHux',
        password='DY6sq7EGkRcraIIC6DoefnvQc',
        account_number=510087100,
        meter_number=119242929,
        name = 'Nazareno',
        number = 1238040913,
        email = 'nazarenoe.ordiz@gmail.com'
        )
    req = requests.post(url, data=post_data, headers=headers)
    obj = xmltodict.parse(req.content)
    ServiceDescription = obj["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ProcessShipmentReply"]["CompletedShipmentDetail"]
    response_dict = {
        'ServiceName': str(ServiceDescription["ServiceDescription"]['Description']),
        'LabelCost': str(ServiceDescription['ShipmentRating']["ShipmentRateDetails"][1]['TotalNetChargeWithDutiesAndTaxes']['Amount']),
        'LabelPdf': (ServiceDescription['CompletedPackageDetails']["Label"]['Parts']['Image']),
    }
    query = '{{ label(ServiceName: "{ServiceName}" LabelCost: "{LabelCost}" LabelPdf: "{LabelPdf}") }}'.format(
        ServiceName=response_dict['ServiceName'],
        LabelCost=response_dict['LabelCost'],
        LabelPdf=response_dict['LabelPdf'],)
    result = schema.execute(query)
    return result.data['label']

schema = graphene.Schema(query=Query)
@app.route("/void", methods=['POST'])

def void():
    url = 'https://wsbeta.fedex.com:443/web-services'
    headers = {
        'Content-Type': 'text/xml'
        }
    post_data = render_template('deleteshipment_Ext_request.xml', key='4UK71Z09zHJvRHux',
        password='DY6sq7EGkRcraIIC6DoefnvQc',
        account_number=510087100,
        meter_number=119242929,
        )
    req = requests.post(url, data=post_data, headers=headers)
    obj = xmltodict.parse(req.content)
    ServiceDescription = obj["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["ShipmentReply"]
    response_dict = {
        'Status': str(ServiceDescription["Notifications"]['Severity']),
        'Message': str(ServiceDescription['Notifications']['Message']),
    }
    query = '{{ void(Status: "{Status}" Message: "{Message}") }}'.format(
        Status=response_dict['Status'],
        Message=response_dict['Message'],)
    result = schema.execute(query)
    return result.data['void']
