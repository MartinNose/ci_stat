import ci_stat.ci_stat as stat
from ci_stat.misc import RedirectStdStreams
import json
import os
import copy
from datetime import datetime,date,timedelta
from ci_stat.feishu_bot import res_to_card, bot_post, add_content
import schedule
import time
from pathlib import Path

def add_job(field, job):
    add_content(field, "\n**" + job.job_name + "** ")
    add_content(field, "**🟢: **"  + str(job.success_cnt) + " ")
    add_content(field, "**🔴: **" + str(job.fail_cnt) + " ")
    add_content(field, "**🟡: **" + str(job.abort_cnt) + " ")
    add_content(field, "**🔄: **" + str(job.rerun_cnt) + " ")
    rerun_list = list(filter(lambda x: x[1].rerun_cnt(job.job_name) > 0, sorted(job.local_prs.items(), key=lambda x: x[1].rerun_cnt(job.job_name), reverse=True)))
    for pr_number, pr in rerun_list[:3]:
        add_content(field, "\n  " + pr.repo + " [#" + str(pr.number) + "]("+pr.link +") **rerun cnt:** " + str(pr.rerun_cnt(job.job_name)))
        run_list = list(filter(lambda x: x.job_name == job.job_name and len(x.get_fail_info()) > 0, pr.runs))
        for run in run_list[:3]:
            fail_infos = run.get_fail_info()
            add_content(field, "\n        [" + str(run.job_id) + "](" + run.link + ") ...**" + "_".join(run.job_name.split('_')[-2:]) + "**: ")
            if len(fail_infos) == 0:
                add_content(field, "Msg Not Found [View Log](" + run.link + ")")
            else:
                for info in fail_infos:
                    add_content(field, "\n             " + info[0])
                    for detail in info[1].split("\n")[:5]:
                        add_content(field, "\n                 " + detail[:83])
                    if len(detail) > 83:
                        add_content(field, " ...")
        if len(pr.runs) > 3 and len(run_list) > 0:
            add_content(field, "\n         ... **" + str(pr.rerun_cnt(job.job_name) + 1 - min(3, len(run_list))) + "** more runs. ")
    if len(rerun_list) > 3:
        add_content(field, "\n... **" + str(len(rerun_list) - 3) + "** *more rerunning prs and totally* **" + str(job.rerun_cnt) + "** *reran runs.*")

def append_rerun(card, res):
    card["elements"][0]["text"]["content"]="**CI Status Daily Report**"
    fields = card["elements"][0]["fields"]
    temp = copy.deepcopy(fields[0])
    temp["text"]["content"] = ""
    fields.insert(6, temp)
    fields.insert(6, copy.deepcopy(temp))

    add_content(fields[6], "**Top Rerunning Job:**")
    job_list = sorted(res.job_map.items(), key=lambda x: x[1].rerun_cnt, reverse=True)
    for job_name, job in job_list[:10]:
        add_job(fields[6], job)

    if len(job_list) > 10:
        add_content(fields[6], "\n... **" + str(len(job_list) - 10) + "** *more rerunning jobs.")
    return card

def main():
    end_time = date.today()
    begin_time = end_time - timedelta(days=1)
    res = stat.get_result(begin_time, end_time)

    stat.(res)

    card = append_rerun(res_to_card(res), res)
    bot_post(card)

def daily_report():
    print((date.today() - timedelta(days=1)).strftime('%Y-%m-%d-%H:%M:%S') + " Dailt report running...", end="")
    Path("/root/ci_stat/daily_log/").mkdir(parents=True, exist_ok=True)
    tmp_res = "/root/ci_stat/daily_log/" + (date.today() - timedelta(days=1)).strftime('%Y-%m-%d-%H:%M:%S') + ".log"
    with RedirectStdStreams(stdout=open(tmp_res, "w")):
        res = main()
    print("done")

if __name__ == "__main__":
    schedule.every().day.at("00:00").do(daily_report)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass

    # main()