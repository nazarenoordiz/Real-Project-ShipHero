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
        cost=String(default_value="ERROR"),
        service=String(default_value="ERROR"),
        pdf=String(default_value="ERROR")        
        )
    def resolve_rate(root, info, items):
        return items
    def resolve_label(root, info, cost, service, pdf):
        return f'Your cost: {cost}, the service name: {service}, and the pdf: {pdf}'


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
    post_data = render_template('US_Express_V26_Ext_Request.xml', key='4UK71Z09zHJvRHux',
        password='DY6sq7EGkRcraIIC6DoefnvQc',
        account_number=510087100,
        meter_number=119242929,
        )
    req = requests.post(url, data=post_data, headers=headers)
    obj = xmltodict.parse(req.content)
    return obj

#    necesitamos pegarle a la api de fedex, retornar los datos, pasarlos por graphql, y hacer la response que necesitamos :v

#    tenemos que armar con graphql que para cada query devuelva los valores necesarios.

#    hay que ver como se puede linkear el flask con el graphql, no queda mucho vamo arriba jajaja.

