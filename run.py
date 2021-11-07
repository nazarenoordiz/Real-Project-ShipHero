from flask import Flask, redirect, url_for, render_template, request, render_template_string
import graphene
from graphene import ObjectType, String, Schema
import xmltodict, json
import requests

app = Flask(__name__)


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    rate = String(
        cose=String(default_value="ERROR"),
        service_name=String(default_value="ERROR"),
        service_used=String(default_value="ERROR"),
        label_pdf=String(default_value="ERROR"),
    )
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_rate(root, info, cose, service_name, service_used, label_pdf):
        return f'Your cose: {cose}, the service name and code: {service_name}-{service_used}, and the transittime: {label_pdf}'

    def resolve_goodbye(root, info):
        return 'See ya!'



schema = graphene.Schema(query=Query)
@app.route("/rates", methods=['POST'])

def rates():
    url = 'https://wsbeta.fedex.com:443/web-services'
    template_data = {
        'key': '4UK71Z09zHJvRHux',
        'password': 'RN2TO13sdEikMHyYkrccW0qW0',
        'account_number': '510087100',
        'meter_number': '119242929'
    }
    headers = {
        'Content-Type': 'text/xml'
        }
    post_data = render_template('RateService_getRates_Request.xml', key='4UK71Z09zHJvRHux',
        password='DY6sq7EGkRcraIIC6DoefnvQc',
        account_number=510087100,
        meter_number=119242929)
    req = requests.post(url, data=post_data, headers=headers)
    obj = xmltodict.parse(req.content)
    ServiceDescription = obj["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["RateReply"]["RateReplyDetails"]["ServiceDescription"]
    response_dict = {
        'cose': 'None',
        'service_name': str(ServiceDescription['Description']),
        'service_code': str(ServiceDescription['Code']),
        'transit_time': None
    }
    query_string = '{{ rate(service_name: "{name}" cose: "{cose}") }}'.format(
        cose=response_dict['cose'], name=response_dict['service_name'])
    result = schema.execute(query_string)
    return result.data['rate']



#    necesitamos pegarle a la api de fedex, retornar los datos, pasarlos por graphql, y hacer la response que necesitamos :v

#    tenemos que armar con graphql que para cada query devuelva los valores necesarios.

#    hay que ver como se puede linkear el flask con el graphql, no queda mucho vamo arriba jajaja.

