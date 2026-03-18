# 0: 命令执行成功
# 1: 命令执行失败
uint8 TASK_SERVICE_RESULT_SUCCESS=0
uint8 TASK_SERVICE_RESULT_FAIL=1
uint8 result

uint32 id
TaskState task_state
uint32 error_code

TaskState state

string message