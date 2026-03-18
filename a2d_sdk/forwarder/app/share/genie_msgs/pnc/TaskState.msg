# frame id 无用, timestamp发送时间
std_msgs/Header header

# Unique identifier for the task
uint32 id

# The current state of the task
uint8 TASK_STATE_IDLE = 0
uint8 TASK_STATE_STARTING = 1
uint8 TASK_STATE_RUNNING = 2
uint8 TASK_STATE_PAUSING = 3
uint8 TASK_STATE_PAUSED = 4
uint8 TASK_STATE_RESUMING = 5
uint8 TASK_STATE_CANCELING = 6
uint8 TASK_STATE_CANCELED = 7
uint8 TASK_STATE_FAIL = 8
uint8 TASK_STATE_SUCCESS = 9
uint8 state

string message

