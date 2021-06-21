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
res = get_result(datetime(2021, 6, 1, 0, 0), datetime.now, [])
```



### `job_list(job_map)`

List all of job in a map from job_id to `job` object in a descending order on fail_cnt.

### `pr_list(pr_map)`

List all of job in a map from pr_id to `pr` object in a descending order on fail_cnt.



## Classes

### Result

[WIP]

### Run

[WIP]

### Commit

[WIP]

### PR

[WIP]

### Job

[WIP]

### Fail_Info

[WIP]



