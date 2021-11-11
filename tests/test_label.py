import json


def test_label(app, client):
    res = client.post('/label')
    assert res.status_code == 200
    assert b'FedEx Home Delivery' in res.data