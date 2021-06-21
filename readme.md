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
      "app_id": "********", # feishu 
      "app_secret": "*********",
      "gh_token": "************" #
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



### Issue Report







## API

### `get_result(begin, end, job_name)`

### `job_list(job_map)`

### `pr_list(pr_map)`



## Classes

### Run



### Commit



### PR



### Job



### Fail_Info





