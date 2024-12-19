# This script is based on the one they created by Masudur Rahaman Sayem, Akeef Khan
# https://aws.amazon.com/jp/blogs/big-data/connect-to-amazon-msk-serverless-from-your-on-premises-network/

from kafka import KafkaProducer
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
import json
import random
import os
from datetime import datetime
topicname='mytopic'

msk_broker = os.environ.get('MSK_BROKER')
region = os.environ.get('AWS_REGION')
class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(region)
        return token

tp = MSKTokenProvider()

producer = KafkaProducer(
    bootstrap_servers=msk_broker,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retry_backoff_ms=500,
    request_timeout_ms=20000,
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,)

# Method to get a random model name
def getModel():
    products=["Ultra WiFi Modem", "Ultra WiFi Booster", "EVG2000", "Sagemcom 5366 TN", "ASUS AX5400"]
    randomnum = random.randint(0, 4)
    return (products[randomnum])

# Method to get a random interface status
def getInterfaceStatus():
    status=["connected", "connected", "connected", "connected", "connected", "connected", "connected", "connected", "connected", "connected", "connected", "connected", "down", "down"]
    randomnum = random.randint(0, 13)
    return (status[randomnum])

# Method to get a random CPU usage
def getCPU():
    i = random.randint(50, 100)
    return (str(i))

# Method to get a random memory usage
def getMemory():
    i = random.randint(1000, 1500)
    return (str(i))
    
# Method to generate sample data
def generateData():
    
    model=getModel()
    deviceid='dvc' + str(random.randint(1000, 10000))
    interface='eth4.1'
    interfacestatus=getInterfaceStatus()
    cpuusage=getCPU()
    memoryusage=getMemory()
    now = datetime.now()
    event_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    modem_data={}
    modem_data["model"]=model
    modem_data["deviceid"]=deviceid
    modem_data["interface"]=interface
    modem_data["interfacestatus"]=interfacestatus
    modem_data["cpuusage"]=cpuusage
    modem_data["memoryusage"]=memoryusage
    modem_data["event_time"]=event_time
    return modem_data

# Continuously generate and send data
while True:
    data =generateData()
    print(data)
    try:
        future = producer.send(topicname, value=data)
        producer.flush()
        record_metadata = future.get(timeout=10)
        
    except Exception as e:
        print(e.with_traceback())