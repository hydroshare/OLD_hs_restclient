hs_restclient
=============

Python client library for HydroShare's REST API

Questions? brian_miles@unc.edu

## To run tests
    python setup.py test

## To use
	from hs_restclient import HydroShare
	
	hs = HydroShare('http://127.0.0.1:8001/api/v1/', user_name='hs', password='water')
	
	res = hs.createResource('created with API', filename='to.zip')
	res.id
	res.title
	
	res2 = hs.getResource(id)
	res
	res2
	res2.title
	
	res2.writeFile('from.zip')