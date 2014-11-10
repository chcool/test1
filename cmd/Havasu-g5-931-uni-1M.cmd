conf
match-list match_931-1
match-rule 1 match vlan 931 remove-tag
top

service-profile svcp_931-1
top

service-instance svcins_931-1 931 svcp_931-1
match-list match_931-1
top

interface ethernet g5
service-role uni
uni
service svcins_931-1
no shut
exit
exit
no shut
end

con
bandwidth-profile 1M
meter MEF
cir 1024
top

service-profile svcp_931-1
valid-service-bandwidth 1M
egress 1M
ingress 1M
top

interface ethernet g5
uni service svcins_931-1
bandwidth 1M
end
c
