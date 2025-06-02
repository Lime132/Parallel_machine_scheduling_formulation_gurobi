import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

"""
M1 ~ M4 & cvxpy, gurobi 
총 8개의 간트차트 그리는 함수들입니다.
"""

def M1_cvxpy_gantt(x, p, J, m):
    """
    M1 - gantt chart 
    """
    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    # 머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 결과 파싱 및 출력
    for (i, j, t), dv in x.items():
        if dv.value >= 1e-6:
            schedule[i + 1].append({
                'job': j + 1,
                'start': t,
                'duration': p[j],
                'color': job_colors[j],
            })

    # Gantt 차트 시각화
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")
        
        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()

def M1_gurobi_gantt(model, p, J, m):
    """
    M1 - gantt chart 
    """
    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    # 머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 결과 파싱 및 출력
    for v in model.getVars():
        if v.x >= 1e-6 and v.varName[0] == 'x':
            i = int(v.varName.split("_")[1])
            j = int(v.varName.split("_")[2])
            t = int(v.varName.split("_")[3])
            schedule[i].append({
                'job': j,
                'start': t,
                'duration': p[j-1],
                'color': job_colors[j-1],
            })

    # Gantt 차트 시각화
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")
        
        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()


def M2_cvxpy_gantt(C, x, p, J, m):
    """
    M2 - gantt chart 
    """

    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    #  머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 작업별 머신 추출
    job_to_machine = {}

    for (i, l, j), dv in x.items():
        if dv.value is not None and dv.value > 1e-6:
            if j != -1:
                job_to_machine[j] = i + 1  # 0-index → 1-index 머신 번호

    # Cj 기반으로 스케줄 구성
    for j in J:
        dv = C.get(j)
        if dv and dv.value is not None and dv.value > 1e-6:
            end = dv.value
            start = end - p[j]

            machine = job_to_machine.get(j)
            schedule[machine].append({
                'job': j + 1,
                'start': start,
                'duration': p[j],
                'color': job_colors[j],
            })

    # Gantt 차트 그리기
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")

        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()

def M2_gurobi_gantt(model, p, J, m):
    """
    M2 - gantt chart 
    """

    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    #  머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 작업별 머신 추출
    job_to_machine = {}

    # 결과 파싱 및 출력
    for v in model.getVars():
        if v.x >= 1e-6 and v.varName[0] == 'x':
            i = int(v.varName.split("_")[1])
            j = int(v.varName.split("_")[2])

            if j != 0:
                job_to_machine[j] = i

    # Cj 기반으로 스케줄 구성
    for v in model.getVars():
        if v.x >= 1e-6 and v.varName[0] == 'C' and v.varName.split("_")[2] != "max":
            j = int(v.varName.split("_")[1])
            end = v.x
            start = end - p[j-1]
            machine = job_to_machine.get(j)
            schedule[machine].append({
                'job': j,
                'start': start,
                'duration': p[j-1],
                'color': job_colors[j-1],
            })
            

    # Gantt 차트 그리기
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")

        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()

def M3_cvxpy_gantt(C, u, p, J, m):
    """
    M3 - gantt chart 
    """

    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    #  머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 작업별 머신 추출
    job_to_machine = {}

    for (i, j, l), dv in u.items():
        if dv.value is not None and dv.value > 1e-6:
            if j != -1:
                job_to_machine[j] = i + 1  # 0-index → 1-index 머신 번호

    # Cj 기반으로 스케줄 구성
    for j in J:
        dv = C.get(j)
        if dv and dv.value is not None and dv.value > 1e-6:
            end = dv.value
            start = end - p[j]

            machine = job_to_machine.get(j)
            schedule[machine].append({
                'job': j + 1,
                'start': start,
                'duration': p[j],
                'color': job_colors[j],
            })

    # Gantt 차트 그리기
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")

        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()

def M3_gurobi_gantt(model, p, J, m):
    """
    M3 - gantt chart 
    """

    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    #  머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 작업별 머신 추출
    job_to_machine = {}

    # 결과 파싱 및 출력
    for v in model.getVars():
        if v.x >= 1e-6 and v.varName[0] == 'u':
            i = int(v.varName.split("_")[1])
            j = int(v.varName.split("_")[2])

            job_to_machine[j] = i

    # Cj 기반으로 스케줄 구성
    for v in model.getVars():
        if v.x >= 1e-6 and v.varName[0] == 'C' and v.varName.split("_")[2] != "max":
            j = int(v.varName.split("_")[1])
            end = v.x
            start = end - p[j-1]
            machine = job_to_machine.get(j)
            schedule[machine].append({
                'job': j,
                'start': start,
                'duration': p[j-1],
                'color': job_colors[j-1],
            })
            

    # Gantt 차트 그리기
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")

        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()


def M4_cvxpy_gantt(C, z, p, J, m):
    """
    M4 - gantt chart 
    """

    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    #  머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 작업별 머신 추출
    job_to_machine = {}

    for (j, i), dv in z.items():
        if dv.value is not None and dv.value > 1e-6:
            if j != -1:
                job_to_machine[j] = i + 1  # 0-index → 1-index 머신 번호

    # Cj 기반으로 스케줄 구성
    for j in J:
        dv = C.get(j)
        if dv and dv.value is not None and dv.value > 1e-6:
            end = dv.value
            start = end - p[j]

            machine = job_to_machine.get(j)
            schedule[machine].append({
                'job': j + 1,
                'start': start,
                'duration': p[j],
                'color': job_colors[j],
            })


    # Gantt 차트 그리기
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")

        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()

def M4_gurobi_gantt(model, p, J, m):
    """
    M4 - gantt chart 
    """

    # 시드 고정하여 작업별 색상 랜덤으로 생성 
    random.seed(917)
    job_colors = {j: "#%06x" % random.randint(0, 0xFFFFFF) for j in J}

    #  머신별 스케줄 초기화
    schedule = {i + 1: [] for i in range(m)}

    # 작업별 머신 추출
    job_to_machine = {}

    # 결과 파싱 및 출력
    for v in model.getVars():
        if v.x >= 1e-6 and v.varName[0] == 'z':
            j = int(v.varName.split("_")[1])
            i = int(v.varName.split("_")[2])

            job_to_machine[j] = i

    # Cj 기반으로 스케줄 구성
    for v in model.getVars():
        if v.x >= 1e-6 and v.varName[0] == 'C' and v.varName.split("_")[2] != "max":
            j = int(v.varName.split("_")[1])
            end = v.x
            start = end - p[j-1]
            machine = job_to_machine.get(j)
            schedule[machine].append({
                'job': j,
                'start': start,
                'duration': p[j-1],
                'color': job_colors[j-1],
            })
            

    # Gantt 차트 그리기
    fig, ax = plt.subplots(figsize=(10, 3 + m))
    yticks = []
    yticklabels = []

    for idx, (machine, tasks) in enumerate(schedule.items()):
        y = m - idx
        yticks.append(y)
        yticklabels.append(f"Machine {machine}")

        for task in tasks:
            ax.barh(
                y=y,
                width=task['duration'],
                left=task['start'],
                height=0.6,
                color=task['color'],
                edgecolor='black'
            )
            ax.text(
                task['start'] + task['duration'] / 2,
                y,
                f"Job {task['job']}",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.set_xlim(0)

    plt.tight_layout()
    plt.show()