import json


def test_void(app, client):
    res = client.post('/void')
    assert res.status_code == 200

def test_void_error(app, client):
    res = client.post('/vooidddd')
    assert res.status_code == 404