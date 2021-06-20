import ci_stat as stat
from ci_stat import get_result, env
from datetime import timedelta, date, datetime
import time
import requests
import schedule
import os.path
import json
from github import Github
import os
from pprint import pprint
import subprocess



def daily_task():
    end_time = datetime.today()
    begin_time = end_time - timedelta(days=1) 
    res = get_result(begin_time, end_time, ["tidb-unit-test-nightly"])

    failed_runs = filter(lambda x: x.case_mark, res.special_list)


def daily_task():
    bug_map = {}
    ghis = requests.get("https://api.github.com/repos/pingcap/tidb/issues", params={'creator':'zhouqiang-cl'}, headers={'Authorization': 'token ' + env["gh_token"]}).json()
    # ghis = requests.get("https://api.github.com/repos/martinnose/ci_stat/issues", params={'creator':'tidb-ci-bot'}, headers={'Authorization': 'token ' + env["gh_token"]}).json()
    ghis = ghis + requests.get("https://api.github.com/repos/pingcap/tidb/issues", params={'creator':'tidb-ci-bot'}, headers={'Authorization': 'token ' + env["gh_token"]}).json()

    for i in filter(lambda x: "`" in x["title"] and "```" in x["body"], ghis):
        title = i["title"].split("`")[1]
        if " " in title:
            title = title.split(" ")[1]
        bug_map[title] = i["body"].split("```")[1]

    end_time = datetime.today()
    begin_time = end_time - timedelta(days=7) 
    res = get_result(begin_time, end_time, ["tidb-unit-test-nightly"])

    failed_runs = filter(lambda x: x.case_mark, res.special_list)
    print(len(list(failed_runs)))
    for run in failed_runs:
        for fail in run.get_fail_info():
            title = fail[0].split(" ")[2]
            log = fail[1]
            print(title)
            if not title in bug_map:
                print("^^^^^^^^^^^^^^^")
                if run.commit is None:
                    cmd = 'cat /mnt/ci.pingcap.net/jenkins_home/jobs/'+ run.job_name + '/builds/'+ str(run.job_id) + '/log ' + '| grep "git checkout" | tail -n1'
                    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    run.commit = ps.communicate()[0].decode("utf-8").split(" ")[-1]
                report(title, log, "master", run.commit, run.link)

def report(title, log, branch, commit, link):
    token = env["gh_token"]

    body = '## Bug Report\r\n```\r\n' \
            + log \
            + '\r\n```\r\nPlease answer these questions before submitting your issue. Thanks!\r\n\r\n### 1. Minimal reproduce step (Required)\r\nin ci '\
            + link \
            + '\r\n\r\n<!-- a step by step guide for reproducing the bug. -->\r\n\r\n### 2. What did you expect to see? (Required)\r\n\r\n### 3. What did you see instead (Required)\r\n\r\n### 4. What is your TiDB version? (Required)\r\n' \
            + branch + " " + commit \
            + '\r\n\r\n<!-- Paste the output of SELECT tidb_version() -->\r\n\r\n'

    client = Github(token)
    repo = client.get_repo("pingcap/tidb")
    # repo = client.get_repo("MartinNose/ci_stat")
    issue = repo.create_issue(
        title="unstable test `" + title + "`",
        body=body,
        labels=[
            repo.get_label("type/bug")
        ]
    )
    pprint(issue)

def main():
    schedule.every().day.at("00:00").do(daily_task)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    # daily_task()
    main()