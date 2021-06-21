import ci_stat as stat
from datetime import timedelta, date, datetime

def main():
    end_time = date.today()
    begin_time = end_time - timedelta(days=7)
    res = stat.get_result(begin_time, end_time, ["tidb_ghpr_check", "tidb_ghpr_check_2", "tidb_ghpr_unit_test", "tidb_ghpr_build"])
    stat.summary(begin_time, end_time, res)

    stat.job_list(res.job_map)    
    stat.pr_list(res.pr_map)

if __name__ == "__main__":
    main()