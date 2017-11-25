sort -o terms_sorted_10.txt terms_10.txt -u 
sort -o years_sorted_10.txt years_10.txt -u 
sort -o recs_sorted_10.txt recs_10.txt -u 
    
perl break.pl < terms_sorted_10.txt > terms_temp.txt
perl break.pl < years_sorted_10.txt > years_temp.txt
perl break.pl < recs_sorted_10.txt > recs_temp.txt

# http://www.perlmonks.org/?node_id=627912
db_load -c duplicates=1 -T -t btree -f terms_temp.txt te.idx
db_load -c duplicates=1 -T -t btree -f years_temp.txt ye.idx
db_load -c duplicates=1 -T -t hash -f recs_temp.txt re.idx

# rm terms_sorted_10.txt
# rm years_sorted_10.txt
# rm recs_sorted_10.txt

# rm terms_temp.txt
# rm years_temp.txt
# rm recs_temp.txt