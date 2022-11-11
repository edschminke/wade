import http.client
import ssl
import base64

# username and password of account with required permissions
username = "schedmaster"
password = "[REDACTED]"

# build the base64 encode credentials string used for HTTP Basic Authentication
credentials = base64.b64encode("{username}:{password}".format(username=username, password=password).encode()).decode("ascii")

# Hostname and port where the EspDSeriesService is located
host = "lxcoswad1d.hfc.ad"
port = 9443
context = ssl.SSLContext()

# This connection test does NOT verify TLS cert presented by host
# This configuration should *not* be used in production
conn = http.client.HTTPSConnection(host, port=port, context=context)

# SOAP requires Content-type: text/xml
# Credentials are passed in HTTP request headers for BASIC Authentication
http_head = {'Content-type': 'text/xml',
             'Authorization': 'Basic %s' % credentials }

# SOAP Message gets passed as HTTP request body
# Example taken from documentation
# https://techdocs.broadcom.com/us/en/ca-enterprise-software/intelligent-automation/ca-workload-automation-de/12-1/utilities-and-soap-web-services-functions/ca-wa-soap-web-services/event-web-services-functions.html
# xmlns:soap modified due to Version mismatch per https://stackoverflow.com/questions/26233636/

http_body = """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://webservice.engine.wa.ca.com/xsd">
	<soap:Header/>
	<soap:Body>
		<xsd:getResourceUsage>
			<xsd:resourceName>ORACLE_EDS</xsd:resourceName>
		</xsd:getResourceUsage>
	</soap:Body>
</soap:Envelope>
"""

conn.request('POST', '/axis2/services/EspDSeriesService?wsdl', http_body, http_head)
resp = conn.getresponse()
print(resp.read().decode())
