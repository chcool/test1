con
ntp server 1
address 10.2.10.10
end

con
@EXP 'list(.*)(: )$'
snmp community-ro
public
end
