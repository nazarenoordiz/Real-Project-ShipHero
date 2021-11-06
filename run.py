from flask import Flask, redirect, url_for, render_template, request, render_template_string
import graphene
import xmltodict, json
import requests
from werkzeug.datastructures import Headers

app = Flask(__name__)


class Query(graphene.ObjectType):
    
    rates = graphene.String(
        label_cost=graphene.Argument(graphene.String, default_value='test'),
        service_used=graphene.Argument(graphene.String, default_value='testing'), 
        label_pdf=graphene.Argument(graphene.String, default_value='tesint')
        )

    def resolve_rates(self, args, context, info):
        return 'Your cose: {}, the service name and code: {}-{}, and the transittime: {}'.format(
            args['label_cost'], args['service_used'], args['label_pdf']
        )


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
    
    return req.content

#    necesitamos pegarle a la api de fedex, retornar los datos, pasarlos por graphql, y hacer la response que necesitamos :v

#    tenemos que armar con graphql que para cada query devuelva los valores necesarios.