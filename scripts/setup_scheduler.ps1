# -*- coding: utf-8 -*-
# setup_scheduler.py — 创建/验证 Windows 计划任务（每天早 8:00）
import subprocess, sys

SCRIPT_DIR = r"C:\Users\wangc\.qclaw\workspace\aiops-hot\scripts"
BAT_PATH = rf"{SCRIPT_DIR}\run_daily.bat"
TASK_NAME = "AIOpsHot_DailyUpdate"

def run_powershell(script: str) -> str:
    result = subprocess.run(
        ["powershell", "-Command", script],
        capture_output=True, text=True
    )
    return result.stdout + result.stderr

# 1. 删除旧任务（如果存在）
print("检查已有计划任务...")
result = run_powershell(
    f'SchTasks /Delete /TN "{TASK_NAME}" /F 2>$null; echo "OK"'
)
print(result.strip())

# 2. 创建新任务
# 触发器: 每天 08:00
cmd = (
    f'SchTasks /Create /TN "{TASK_NAME}" '
    f'/TR \'"%COMSPEC%" /c "{BAT_PATH}"\' '
    f'/SC DAILY /ST 08:00 '
    f'/RL HIGHEST /F'
)
print(f"\n创建计划任务: 每天 08:00 执行 {BAT_PATH}")
result = run_powershell(cmd)
print(result)

if "ERROR" in result or "错误" in result:
    print("\n[WARNING] 需要管理员权限，尝试使用当前用户权限...")
    cmd2 = (
        f'SchTasks /Create /TN "{TASK_NAME}" '
        f'/TR \'"%COMSPEC%" /c "{BAT_PATH}"\' '
        f'/SC DAILY /ST 08:00 /F'
    )
    result2 = run_powershell(cmd2)
    print(result2)

# 3. 验证
print("\n验证任务创建结果:")
verify = run_powershell(f'SchTasks /Query /TN "{TASK_NAME}" 2>&1')
print(verify[:500])

print("\n[完成] 计划任务已设置，每天早 8:00 自动更新！")
