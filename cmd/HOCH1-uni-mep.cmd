conf
match-list match_untag
match-rule 1 match untagged
top

service-profile svcp_931
top

service-instance svcins_931 931 svcp_931
top

interface ethernet e3
no shut
service-role uni
uni
service svcins_931 match-list match_untag
no shut
end

