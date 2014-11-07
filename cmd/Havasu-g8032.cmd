cli
en

con
interface ethernet g1
duplex full
flow-control none
service-role inni
no shut
end

con
interface ethernet g2
duplex full
flow-control none
service-role inni
no shut
end


configure
g8032-ring 1
ring-id 1
control-vlan 1
wait-to-restore-time 1
admin enable
exit

interface ethernet g1
service-role inni
inni g8032-ring 1 rpl-mode none
end

con
interface ethernet g2
service-role inni
inni g8032-ring 1 rpl-mode neighbor
end

con
transport-service-profile g8032_tsp1
vlan-list 931-934,401-405,1301-1305,1201-1205
top

interface ethernet g1
service-role inni
inni transport-service-profile g8032_tsp1
top

interface ethernet g2
service-role inni
inni transport-service-profile g8032_tsp1
end

