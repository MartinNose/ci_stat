# **README**

**ci_stat** provides some handy scripts to profile the records in the `sync_ci_data`, including 

- Fetching and listing information of runs, jobs, pull requests
- Sending status report to Feishu hourly and daily.
- Creating corresponding issue when `tide-unit-test-nightly` fails.

And currently **ci_stat** can only run on the machine where the jenkins logs are.

## Environment Set Up

Environment variable:

- `STAT_ENV_PATH`

  Path to `env.json`
- `env.json` (at `$STAT_ENV_PATH`)

  ```json
  {
      "host": "172.*.*.*",
      "port": "***",
      "user": "",
      "password": "",
      "database": "sync_ci_data",
      "log_dir": "",
      "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/*****",
      "app_id": "********",
      "app_secret": "*********",
      "gh_token": "************"
  }
  ```



## Basic Usage

### Fetch and List

Following example log all information of ci during 2021-6-19 to 2021-6-21.

It is recommended to redirect the output to an `.ans` file and open with vscode, which supports escape sequence highlight and folding. 

```shell
python3 example.py > log.ans
```

```python
import ci_stat.ci_stat as stat
from datetime import datetime

begin = datetime(2021, 6, 19, 0, 0)
end = datetime(2021, 6, 21, 0, 0)

res = stat.get_result(begin, end, []) 
stat.summary(res) 					 # Show brief summary of ci status during the time
stat.job_list(res.job_map)	 # List all the jobs executed during the time
stat.pr_list(res.pr_map) 		 # List all the pull requests triggering ci jobs
```

![image-20210621170319212](https://tva1.sinaimg.cn/large/008i3skNly1grpzx67rioj31fx0u0e5o.jpg)![image-20210621170450090](https://tva1.sinaimg.cn/large/008i3skNly1grpzykkq0xj31d10u01kx.jpg)

### Feishu Bot

`ci_stat.feishu_bot` provides following APIs:

- `res_to_card` to convert `res` to a feishu message card.
- `post_card` to send a feishu message card to some group chat.

Example usage can be found at `example_bot.py`.

### Issue Report

`ci_stat.bug_report` provides an API to collect failed runs of job `tide-unit-test-nightly`. `bug_report` first gets all existing issue in repo `PingCAP/TiDB` and failed cases during previous day, then it create new issues for the unreported fail cases.

## API of ci_stat

### `get_result(begin, end, job_name)`

Return a `Result` object. `job_name` is a list of wanted repos, empty job_name means fetch ci data of all repo.

#### Example

```python
res = get_result(
  datetime(2021, 6, 1, 0, 0), 
  datetime.now, 
  [])
```



### `job_list(job_map)`

List all of job in a map from job_id to `job` object in a descending order on fail_cnt.



### `pr_list(pr_map)`

List all of job in a map from pr_id to `pr` object in a descending order on fail_cnt.



## Classes

**claim:** following document only focus on attribute of classes in ci_stat. if not specify, most methods are private and the print/log method is only for your reference, I think it is better to sperate this logging code from the objects because ci_stat is meanly for fetching and storing data. The manipulation process might be done explictly rather than put in a hard-to-customize print/log method.

### Run

Describe a specific run of a job, build up from a record in the table `sync_ci_data`.

Attributes:

- `job_id` , `job_name`
- `status`
- `time`, `duration`
- `comment`
- `repo`, `branch`
- `description`: a column in the table, containing the information of the pr (author, link, content, etc. )
- `pr_number`, `author`, `pr_link`
- `fail_info`: grep from log of this run, is a list of 2-tuple (case_name, error_message)

And for some special run like runs of `tidb-unit-test-nightly`, many information including `pr`, `commit` are missing. Such runs contains:

- `case`: a list of failed case, could be None.

### Commit

Describe a commit and keep track of runs related to this commit

Attributes:

- `hash`, `repo`, `branch`, `pr_number`
- `pr`: a PR objects
- `jobs`: a list of Job objects

- `fail_cnt`, `success_cnt`, `abort_cnt`

### PR

Describe a pull request and keep track of runs related to this PR

Attributes:

- `number`: pr_number
- `repo`, `branch`, `title`, `link`
- `fail_cnt`, `success_cnt`, `abort_cnt`
- `fail_info_map`: a map from fail_case to Fail_Info object
- `commit_hashes`: a list of commit object
- `runs`: a list of runs related to this pr
- `total_rerun_cnt`

Methods:

- `rerun_cnt(job_name: String)`

  Return number of rerun on `$(job_name)` caused by this pr

### Job

Describe a job and keep track of prs related to this job

Attributes:

- `job_name`, `repo`, `branch`
- `prs`: a map from pr_number to a pr object * Might be a bug?
- `local_prs`: a map from pr_number to a pr object that such pr objects contains only runs of this job, making it easier for logging and statisticizing.

### Fail_Info

Describte a fail case and keep track of related runs

Attributes:

- `info`: fail case name
- `run_list`: failed run objects containing this fail info

### Result

Describe results of a fetch and analysis process. 

Attributes:

- `begin_time`, `end_time`
- `run_list`: list of run object
- `special_list`: list of nightly run object, orthogonal to `run_list`
- `miss_cnt`: number of runs failed to grep "----" type fail info
- `fail_cnt`, `success_cnt`, `abort_cnt`, `total_cnt`
- `pr_map`: a map from pr_number to pr objects
- `job_map`: job_name to job object
- `fail_info_map`: fail info name (one line) to fail info object
- `commit_hash_map`: hash to commit object
