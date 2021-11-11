import json


def test_rates(app, client):
    res = client.post('/rates')
    assert res.status_code == 200
    assert b'Priority Overnight' in res.data