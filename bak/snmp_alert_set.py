from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.proto import rfc1902

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

#
# SNMPv3/USM setup
#

# user: Administrator, auth: SHA, priv AES
config.addV3User(
    snmpEngine, 'Administrator',#username
    config.usmHMACSHAAuthProtocol,#authProtocol,sha
     'Admin@9000',#authKey
    config.usmAesCfb128Protocol,#privProtocol,aes
     'Admin@9000' #privKey
)
config.addTargetParams(snmpEngine, 'my-creds', 'Administrator', 'authPriv')

#
# Setup transport endpoint and bind it with security settings yielding
# a target name (choose one entry depending of the transport needed).
#

# UDP/IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
)
config.addTargetAddr(
    snmpEngine, 'my-router',
    udp.domainName, ('10.100.17.135', 161),
    'my-creds'
)

# Error/response reciever
def get_cpu_vendor_cb(sendRequestHandle,
          errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for oid, val in varBindTable:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

# Prepare and send a request message
# get cpu vendor
cmdgen.GetCommandGenerator().sendReq(
    snmpEngine,
    'my-router',
    ( (( 1,3,6,1,4,1,2011,2,235,1,1,15,50,1,2,2), None), ),
    get_cpu_vendor_cb
)


# Error/response reciever
def set_trap_target_addr_cb(sendRequestHandle,
          errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for oid, val in varBindTable:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

# Prepare and send a request message
#set trap target is '1.1.1.1'
# .1.3.6.1.4.1.2011.2.235.1.1.4.50.1.3.1 s "10.100.206.223"
cmdgen.SetCommandGenerator().sendReq(
    snmpEngine,
    'my-router',
    ( (( 1,3,6,1,4,1,2011,2,235,1,1,4,50,1,3,1), rfc1902.OctetString('10.100.206.223')), ),
    set_trap_target_addr_cb
)

# Run I/O dispatcher which would send pending queries and process responses
snmpEngine.transportDispatcher.runDispatcher()
