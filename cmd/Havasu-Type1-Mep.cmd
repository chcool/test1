cli
en

con
ntp server 1
address 10.2.10.10
end

con
snmp community-ro
public
end

conf
match-list match_301
match-rule 1 match vlan 301
top

service-profile svcp_932
top

service-instance svcins_932 932 svcp_932 
match-list match_301
top

interface ethernet g16
service-role uni
uni
service svcins_932
no shut
exit
exit
no shut
end

con
meg V932-EVC-lv4
level 4
mep 216
remote-mep 208
top

service-instance svcins_932 932 svcp_932 
meg V932-EVC-lv4
top

interface ethernet g16
uni service svcins_932
mep V932-EVC-lv4 216
end

con
meg V932-EVC-lv4
mep 216
continuity-check enable
end

