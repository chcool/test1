con
auto-prov disable
top
interface ethernet g3
shut
top
interface ethernet g4
shut
end

conf
match-list match_untag
match-rule 1 match untagged
top

service-profile svcp_931
top

service-instance svcins_931 931 svcp_931
match-list match_untag
top

interface ethernet e1
service-role uni
uni
service svcins_931
no shut
exit
exit
no shut
top

con
meg V931-EVC-lv4
level 4
mep 401
continuity-check enable
remote-mep 403
top

service-instance svcins_931 931 svcp_931
meg V931-EVC-lv4
top

interface ethernet e1
uni service svcins_931
mep V931-EVC-lv4 401
end



