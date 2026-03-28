import sqlite3
import datetime
import os

# 创建数据库连接
def create_connection():
    conn = sqlite3.connect('attendance.db')
    return conn

# 初始化数据库
def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    # 创建打卡记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clock_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        clock_time DATETIME NOT NULL,
        clock_type TEXT NOT NULL,
        location TEXT,
        status TEXT DEFAULT '正常',
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 创建补卡申请表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supplement_apply (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        apply_date DATE NOT NULL,
        clock_type TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT DEFAULT '待审批',
        approver_id INTEGER,
        approval_time TIMESTAMP,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 创建请假/加班申请表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_apply (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        apply_type TEXT NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        duration REAL NOT NULL,
        reason TEXT NOT NULL,
        status TEXT DEFAULT '待审批',
        approver_id INTEGER,
        approval_time TIMESTAMP,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 创建调休/出差申请表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS adjust_apply (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        apply_type TEXT NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        duration REAL NOT NULL,
        reason TEXT NOT NULL,
        status TEXT DEFAULT '待审批',
        approver_id INTEGER,
        approval_time TIMESTAMP,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 创建考勤确认表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance_confirm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        confirm_month TEXT NOT NULL,
        status TEXT DEFAULT '待确认',
        confirm_time TIMESTAMP,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

# 打卡功能
def add_clock_record(user_id, user_name, clock_type, location):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clock_record (user_id, user_name, clock_time, clock_type, location) VALUES (?, ?, ?, ?, ?)",
        (user_id, user_name, datetime.datetime.now(), clock_type, location)
    )
    conn.commit()
    conn.close()

# 获取打卡记录
def get_clock_records(user_id, start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM clock_record WHERE user_id = ? AND DATE(clock_time) BETWEEN ? AND ? ORDER BY clock_time DESC",
        (user_id, start_date, end_date)
    )
    records = cursor.fetchall()
    conn.close()
    return records

# 补卡申请
def add_supplement_apply(user_id, user_name, apply_date, clock_type, reason):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO supplement_apply (user_id, user_name, apply_date, clock_type, reason) VALUES (?, ?, ?, ?, ?)",
        (user_id, user_name, apply_date, clock_type, reason)
    )
    conn.commit()
    conn.close()

# 获取补卡申请
def get_supplement_applies(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM supplement_apply WHERE user_id = ? ORDER BY create_time DESC",
        (user_id,)
    )
    records = cursor.fetchall()
    conn.close()
    return records

# 请假/加班申请
def add_leave_apply(user_id, user_name, apply_type, start_time, end_time, duration, reason):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leave_apply (user_id, user_name, apply_type, start_time, end_time, duration, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, user_name, apply_type, start_time, end_time, duration, reason)
    )
    conn.commit()
    conn.close()

# 获取请假/加班申请
def get_leave_applies(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM leave_apply WHERE user_id = ? ORDER BY create_time DESC",
        (user_id,)
    )
    records = cursor.fetchall()
    conn.close()
    return records

# 调休/出差申请
def add_adjust_apply(user_id, user_name, apply_type, start_time, end_time, duration, reason):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO adjust_apply (user_id, user_name, apply_type, start_time, end_time, duration, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, user_name, apply_type, start_time, end_time, duration, reason)
    )
    conn.commit()
    conn.close()

# 获取调休/出差申请
def get_adjust_applies(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM adjust_apply WHERE user_id = ? ORDER BY create_time DESC",
        (user_id,)
    )
    records = cursor.fetchall()
    conn.close()
    return records

# 考勤确认
def add_attendance_confirm(user_id, user_name, confirm_month):
    conn = create_connection()
    cursor = conn.cursor()
    # 检查是否已存在
    cursor.execute(
        "SELECT * FROM attendance_confirm WHERE user_id = ? AND confirm_month = ?",
        (user_id, confirm_month)
    )
    existing = cursor.fetchone()
    if not existing:
        cursor.execute(
            "INSERT INTO attendance_confirm (user_id, user_name, confirm_month, status, confirm_time) VALUES (?, ?, ?, ?, ?)",
            (user_id, user_name, confirm_month, '已确认', datetime.datetime.now())
        )
        conn.commit()
    conn.close()

# 获取考勤确认
def get_attendance_confirms(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM attendance_confirm WHERE user_id = ? ORDER BY confirm_month DESC",
        (user_id,)
    )
    records = cursor.fetchall()
    conn.close()
    return records

# 主菜单
def main_menu():
    print("\n" + "="*50)
    print("考勤管理系统")
    print("="*50)
    print("1. 打卡管理")
    print("2. 补卡申请")
    print("3. 请假/加班")
    print("4. 调休/出差")
    print("5. 考勤确认")
    print("0. 退出系统")
    print("="*50)
    choice = input("请选择功能序号: ")
    return choice

# 打卡管理菜单
def clock_menu(user_id, user_name):
    while True:
        print("\n" + "-"*50)
        print("打卡管理")
        print("-"*50)
        print("1. 上班打卡")
        print("2. 下班打卡")
        print("3. 查看打卡记录")
        print("0. 返回主菜单")
        choice = input("请选择功能序号: ")
        
        if choice == "1":
            add_clock_record(user_id, user_name, "上班", "办公室")
            print("上班打卡成功！")
        elif choice == "2":
            add_clock_record(user_id, user_name, "下班", "办公室")
            print("下班打卡成功！")
        elif choice == "3":
            start_date = input("请输入开始日期 (YYYY-MM-DD): ")
            end_date = input("请输入结束日期 (YYYY-MM-DD): ")
            records = get_clock_records(user_id, start_date, end_date)
            if records:
                print("\n打卡记录:")
                print("-"*80)
                print(f"{'打卡时间':<20} {'打卡类型':<10} {'打卡地点':<15} {'状态':<10}")
                print("-"*80)
                for record in records:
                    print(f"{record[3]:<20} {record[4]:<10} {record[5]:<15} {record[6]:<10}")
                print("-"*80)
            else:
                print("没有找到打卡记录")
        elif choice == "0":
            break
        else:
            print("输入错误，请重新选择！")

# 补卡申请菜单
def supplement_menu(user_id, user_name):
    while True:
        print("\n" + "-"*50)
        print("补卡申请")
        print("-"*50)
        print("1. 提交补卡申请")
        print("2. 查看补卡记录")
        print("0. 返回主菜单")
        choice = input("请选择功能序号: ")
        
        if choice == "1":
            apply_date = input("请输入申请日期 (YYYY-MM-DD): ")
            clock_type = input("请选择打卡类型 (1.上班 2.下班): ")
            clock_type = "上班" if clock_type == "1" else "下班"
            reason = input("请输入申请原因: ")
            add_supplement_apply(user_id, user_name, apply_date, clock_type, reason)
            print("补卡申请提交成功！")
        elif choice == "2":
            records = get_supplement_applies(user_id)
            if records:
                print("\n补卡申请记录:")
                print("-"*100)
                print(f"{'申请日期':<15} {'打卡类型':<10} {'申请原因':<30} {'状态':<10} {'审批时间':<20}")
                print("-"*100)
                for record in records:
                    print(f"{record[3]:<15} {record[4]:<10} {record[5]:<30} {record[6]:<10} {record[8] if record[8] else '-':<20}")
                print("-"*100)
            else:
                print("没有补卡申请记录")
        elif choice == "0":
            break
        else:
            print("输入错误，请重新选择！")

# 请假/加班菜单
def leave_menu(user_id, user_name):
    while True:
        print("\n" + "-"*50)
        print("请假/加班申请")
        print("-"*50)
        print("1. 提交申请")
        print("2. 查看申请记录")
        print("0. 返回主菜单")
        choice = input("请选择功能序号: ")
        
        if choice == "1":
            apply_type = input("请选择申请类型 (1.请假 2.加班): ")
            apply_type = "请假" if apply_type == "1" else "加班"
            start_time = input("请输入开始时间 (YYYY-MM-DD HH:MM): ")
            end_time = input("请输入结束时间 (YYYY-MM-DD HH:MM): ")
            duration = float(input("请输入时长(小时): "))
            reason = input("请输入申请原因: ")
            add_leave_apply(user_id, user_name, apply_type, start_time, end_time, duration, reason)
            print(f"{apply_type}申请提交成功！")
        elif choice == "2":
            records = get_leave_applies(user_id)
            if records:
                print("\n请假/加班申请记录:")
                print("-"*120)
                print(f"{'申请类型':<10} {'开始时间':<20} {'结束时间':<20} {'时长(小时)':<10} {'申请原因':<30} {'状态':<10}")
                print("-"*120)
                for record in records:
                    print(f"{record[3]:<10} {record[4]:<20} {record[5]:<20} {record[6]:<10} {record[7]:<30} {record[8]:<10}")
                print("-"*120)
            else:
                print("没有请假/加班申请记录")
        elif choice == "0":
            break
        else:
            print("输入错误，请重新选择！")

# 调休/出差菜单
def adjust_menu(user_id, user_name):
    while True:
        print("\n" + "-"*50)
        print("调休/出差申请")
        print("-"*50)
        print("1. 提交申请")
        print("2. 查看申请记录")
        print("0. 返回主菜单")
        choice = input("请选择功能序号: ")
        
        if choice == "1":
            apply_type = input("请选择申请类型 (1.调休 2.出差): ")
            apply_type = "调休" if apply_type == "1" else "出差"
            start_time = input("请输入开始时间 (YYYY-MM-DD HH:MM): ")
            end_time = input("请输入结束时间 (YYYY-MM-DD HH:MM): ")
            duration = float(input("请输入时长(小时): "))
            reason = input("请输入申请原因: ")
            add_adjust_apply(user_id, user_name, apply_type, start_time, end_time, duration, reason)
            print(f"{apply_type}申请提交成功！")
        elif choice == "2":
            records = get_adjust_applies(user_id)
            if records:
                print("\n调休/出差申请记录:")
                print("-"*120)
                print(f"{'申请类型':<10} {'开始时间':<20} {'结束时间':<20} {'时长(小时)':<10} {'申请原因':<30} {'状态':<10}")
                print("-"*120)
                for record in records:
                    print(f"{record[3]:<10} {record[4]:<20} {record[5]:<20} {record[6]:<10} {record[7]:<30} {record[8]:<10}")
                print("-"*120)
            else:
                print("没有调休/出差申请记录")
        elif choice == "0":
            break
        else:
            print("输入错误，请重新选择！")

# 考勤确认菜单
def confirm_menu(user_id, user_name):
    while True:
        print("\n" + "-"*50)
        print("考勤确认")
        print("-"*50)
        print("1. 确认考勤")
        print("2. 查看确认记录")
        print("0. 返回主菜单")
        choice = input("请选择功能序号: ")
        
        if choice == "1":
            confirm_month = input("请输入确认月份 (YYYY-MM): ")
            add_attendance_confirm(user_id, user_name, confirm_month)
            print("考勤确认成功！")
        elif choice == "2":
            records = get_attendance_confirms(user_id)
            if records:
                print("\n考勤确认记录:")
                print("-"*60)
                print(f"{'确认月份':<15} {'状态':<10} {'确认时间':<20}")
                print("-"*60)
                for record in records:
                    print(f"{record[3]:<15} {record[4]:<10} {record[5] if record[5] else '-':<20}")
                print("-"*60)
            else:
                print("没有考勤确认记录")
        elif choice == "0":
            break
        else:
            print("输入错误，请重新选择！")

# 主程序
def main():
    # 初始化数据库
    init_db()
    
    # 用户信息
    user_id = 1
    user_name = "测试用户"
    
    print(f"欢迎使用考勤管理系统，{user_name}！")
    
    while True:
        choice = main_menu()
        
        if choice == "1":
            clock_menu(user_id, user_name)
        elif choice == "2":
            supplement_menu(user_id, user_name)
        elif choice == "3":
            leave_menu(user_id, user_name)
        elif choice == "4":
            adjust_menu(user_id, user_name)
        elif choice == "5":
            confirm_menu(user_id, user_name)
        elif choice == "0":
            print("感谢使用考勤管理系统，再见！")
            break
        else:
            print("输入错误，请重新选择！")

if __name__ == "__main__":
    main()
