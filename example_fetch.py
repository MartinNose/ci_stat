import ci_stat.ci_stat as stat
from datetime import timedelta, date, datetime

begin = datetime(2021, 6, 15, 0, 0)
end = datetime(2021, 6, 15, 12, 00)

res = stat.get_result(begin, end, ["tidb_ghpr_check", "tidb_ghpr_check_2", "tidb_ghpr_unit_test", "tidb_ghpr_build"])

# stat.summary(res)
# stat.job_list(res.job_map)    
stat.pr_list(res.pr_map)