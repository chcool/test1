snmpwalk -v 2c -c public123 <hostname> 1.3.6.1.2.1.47
@wait 3
snmpwalk -v 2c -c public123 <hostname> 1.3.6.1.2.1.99
@wait 3
snmpwalk -v 2c -c public123 <hostname> 1.3.6.1.2.1.131

