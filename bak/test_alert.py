from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('10.100.206.223', 162))
)

# SNMPv3/USM setup

config.addV3User(
    snmpEngine, 'Administrator',
    config.usmHMACSHAAuthProtocol,#authProtocol,sha
     'Admin@9000',#authKey
    config.usmAesCfb128Protocol,#privProtocol,aes
     'Admin@9000', #privKey
    contextEngineId=v2c.OctetString(hexValue='8000000001020304')
)

# Callback function for receiving notifications
def cbFun(snmpEngine,
          stateReference,
          contextEngineId, contextName,
          varBinds,
          cbCtx):
    print('Notification received, ContextEngineId "%s", ContextName "%s"' % (
        contextEngineId.prettyPrint(), contextName.prettyPrint()
        )
    )
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
