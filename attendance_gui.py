import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, 
    QDateTimeEdit, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox
)
from PyQt5.QtCore import QDate, QDateTime

# 创建数据库连接
def create_connection():
    conn = sqlite3.connect('attendance.db')
    return conn

# 初始化数据库
def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user' -- 'admin' 或 'user'
    )''')
    
    # 插入默认管理员和测试用户
    cursor.execute("INSERT OR IGNORE INTO user (username, password, name, role) VALUES ('admin', 'admin123', '管理员', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO user (username, password, name, role) VALUES ('user', 'user123', '测试用户', 'user')")
    
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

# 用户登录验证
def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, name, role FROM user WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user

# 审批申请
def approve_apply(table_name, apply_id, approver_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {table_name} SET status = '已批准', approver_id = ?, approval_time = ? WHERE id = ?",
        (approver_id, datetime.datetime.now(), apply_id)
    )
    conn.commit()
    conn.close()

# 拒绝申请
def reject_apply(table_name, apply_id, approver_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {table_name} SET status = '已拒绝', approver_id = ?, approval_time = ? WHERE id = ?",
        (approver_id, datetime.datetime.now(), apply_id)
    )
    conn.commit()
    conn.close()

# 获取所有申请（管理员用）
def get_all_applies(table_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY create_time DESC")
    records = cursor.fetchall()
    conn.close()
    return records

# 打卡管理界面
class ClockWidget(QWidget):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 打卡按钮
        button_layout = QHBoxLayout()
        self.clock_in_btn = QPushButton("上班打卡")
        self.clock_out_btn = QPushButton("下班打卡")
        self.refresh_btn = QPushButton("刷新")
        button_layout.addWidget(self.clock_in_btn)
        button_layout.addWidget(self.clock_out_btn)
        button_layout.addWidget(self.refresh_btn)
        layout.addLayout(button_layout)
        
        # 日期选择
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("开始日期:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("结束日期:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.end_date)
        self.query_btn = QPushButton("查询")
        date_layout.addWidget(self.query_btn)
        layout.addLayout(date_layout)
        
        # 打卡记录表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["打卡时间", "打卡类型", "打卡地点", "状态"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # 绑定事件
        self.clock_in_btn.clicked.connect(self.clock_in)
        self.clock_out_btn.clicked.connect(self.clock_out)
        self.query_btn.clicked.connect(self.query_records)
        self.refresh_btn.clicked.connect(self.query_records)
    
    def clock_in(self):
        add_clock_record(self.user_id, self.user_name, "上班", "办公室")
        QMessageBox.information(self, "提示", "上班打卡成功！")
    
    def clock_out(self):
        add_clock_record(self.user_id, self.user_name, "下班", "办公室")
        QMessageBox.information(self, "提示", "下班打卡成功！")
    
    def query_records(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        records = get_clock_records(self.user_id, start, end)
        
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(str(record[3])))
            self.table.setItem(i, 1, QTableWidgetItem(record[4]))
            self.table.setItem(i, 2, QTableWidgetItem(record[5]))
            self.table.setItem(i, 3, QTableWidgetItem(record[6]))

# 补卡申请界面
class SupplementWidget(QWidget):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 补卡表单
        form_layout = QVBoxLayout()
        
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("申请日期:"))
        self.apply_date = QDateEdit()
        self.apply_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.apply_date)
        form_layout.addLayout(date_layout)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("打卡类型:"))
        self.clock_type = QComboBox()
        self.clock_type.addItems(["上班", "下班"])
        type_layout.addWidget(self.clock_type)
        form_layout.addLayout(type_layout)
        
        reason_layout = QHBoxLayout()
        reason_layout.addWidget(QLabel("申请原因:"))
        self.reason = QTextEdit()
        reason_layout.addWidget(self.reason)
        form_layout.addLayout(reason_layout)
        
        self.submit_btn = QPushButton("提交申请")
        self.refresh_btn = QPushButton("刷新")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addWidget(self.refresh_btn)
        form_layout.addLayout(btn_layout)
        layout.addLayout(form_layout)
        
        # 申请记录表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["申请日期", "打卡类型", "申请原因", "状态", "审批时间"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # 绑定事件
        self.submit_btn.clicked.connect(self.submit_apply)
        self.refresh_btn.clicked.connect(self.load_records)
        self.load_records()
    
    def submit_apply(self):
        date = self.apply_date.date().toString("yyyy-MM-dd")
        clock_type = self.clock_type.currentText()
        reason = self.reason.toPlainText()
        
        if not reason:
            QMessageBox.warning(self, "警告", "请输入申请原因")
            return
        
        add_supplement_apply(self.user_id, self.user_name, date, clock_type, reason)
        QMessageBox.information(self, "提示", "补卡申请提交成功！")
        self.reason.clear()
        self.load_records()
    
    def load_records(self):
        records = get_supplement_applies(self.user_id)
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(str(record[3])))
            self.table.setItem(i, 1, QTableWidgetItem(record[4]))
            self.table.setItem(i, 2, QTableWidgetItem(record[5]))
            self.table.setItem(i, 3, QTableWidgetItem(record[6]))
            self.table.setItem(i, 4, QTableWidgetItem(str(record[8]) if record[8] else "-"))

# 请假/加班申请界面
class LeaveWidget(QWidget):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 申请表单
        form_layout = QVBoxLayout()
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("申请类型:"))
        self.apply_type = QComboBox()
        self.apply_type.addItems(["请假", "加班"])
        type_layout.addWidget(self.apply_type)
        form_layout.addLayout(type_layout)
        
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("开始时间:"))
        self.start_time = QDateTimeEdit()
        self.start_time.setDateTime(QDateTime.currentDateTime())
        start_layout.addWidget(self.start_time)
        form_layout.addLayout(start_layout)
        
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("结束时间:"))
        self.end_time = QDateTimeEdit()
        self.end_time.setDateTime(QDateTime.currentDateTime())
        end_layout.addWidget(self.end_time)
        form_layout.addLayout(end_layout)
        
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("时长(小时):"))
        self.duration = QLineEdit()
        duration_layout.addWidget(self.duration)
        form_layout.addLayout(duration_layout)
        
        reason_layout = QHBoxLayout()
        reason_layout.addWidget(QLabel("申请原因:"))
        self.reason = QTextEdit()
        reason_layout.addWidget(self.reason)
        form_layout.addLayout(reason_layout)
        
        self.submit_btn = QPushButton("提交申请")
        self.refresh_btn = QPushButton("刷新")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addWidget(self.refresh_btn)
        form_layout.addLayout(btn_layout)
        layout.addLayout(form_layout)
        
        # 申请记录表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["申请类型", "开始时间", "结束时间", "时长(小时)", "申请原因", "状态"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # 绑定事件
        self.submit_btn.clicked.connect(self.submit_apply)
        self.refresh_btn.clicked.connect(self.load_records)
        self.load_records()
    
    def submit_apply(self):
        apply_type = self.apply_type.currentText()
        start = self.start_time.dateTime().toString("yyyy-MM-dd HH:mm")
        end = self.end_time.dateTime().toString("yyyy-MM-dd HH:mm")
        try:
            duration = float(self.duration.text())
        except:
            QMessageBox.warning(self, "警告", "请输入有效的时长")
            return
        reason = self.reason.toPlainText()
        
        if not reason:
            QMessageBox.warning(self, "警告", "请输入申请原因")
            return
        
        add_leave_apply(self.user_id, self.user_name, apply_type, start, end, duration, reason)
        QMessageBox.information(self, "提示", f"{apply_type}申请提交成功！")
        self.duration.clear()
        self.reason.clear()
        self.load_records()
    
    def load_records(self):
        records = get_leave_applies(self.user_id)
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(record[3]))
            self.table.setItem(i, 1, QTableWidgetItem(str(record[4])))
            self.table.setItem(i, 2, QTableWidgetItem(str(record[5])))
            self.table.setItem(i, 3, QTableWidgetItem(str(record[6])))
            self.table.setItem(i, 4, QTableWidgetItem(record[7]))
            self.table.setItem(i, 5, QTableWidgetItem(record[8]))

# 调休/出差申请界面
class AdjustWidget(QWidget):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 申请表单
        form_layout = QVBoxLayout()
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("申请类型:"))
        self.apply_type = QComboBox()
        self.apply_type.addItems(["调休", "出差"])
        type_layout.addWidget(self.apply_type)
        form_layout.addLayout(type_layout)
        
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("开始时间:"))
        self.start_time = QDateTimeEdit()
        self.start_time.setDateTime(QDateTime.currentDateTime())
        start_layout.addWidget(self.start_time)
        form_layout.addLayout(start_layout)
        
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("结束时间:"))
        self.end_time = QDateTimeEdit()
        self.end_time.setDateTime(QDateTime.currentDateTime())
        end_layout.addWidget(self.end_time)
        form_layout.addLayout(end_layout)
        
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("时长(小时):"))
        self.duration = QLineEdit()
        duration_layout.addWidget(self.duration)
        form_layout.addLayout(duration_layout)
        
        reason_layout = QHBoxLayout()
        reason_layout.addWidget(QLabel("申请原因:"))
        self.reason = QTextEdit()
        reason_layout.addWidget(self.reason)
        form_layout.addLayout(reason_layout)
        
        self.submit_btn = QPushButton("提交申请")
        self.refresh_btn = QPushButton("刷新")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addWidget(self.refresh_btn)
        form_layout.addLayout(btn_layout)
        layout.addLayout(form_layout)
        
        # 申请记录表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["申请类型", "开始时间", "结束时间", "时长(小时)", "申请原因", "状态"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # 绑定事件
        self.submit_btn.clicked.connect(self.submit_apply)
        self.refresh_btn.clicked.connect(self.load_records)
        self.load_records()
    
    def submit_apply(self):
        apply_type = self.apply_type.currentText()
        start = self.start_time.dateTime().toString("yyyy-MM-dd HH:mm")
        end = self.end_time.dateTime().toString("yyyy-MM-dd HH:mm")
        try:
            duration = float(self.duration.text())
        except:
            QMessageBox.warning(self, "警告", "请输入有效的时长")
            return
        reason = self.reason.toPlainText()
        
        if not reason:
            QMessageBox.warning(self, "警告", "请输入申请原因")
            return
        
        add_adjust_apply(self.user_id, self.user_name, apply_type, start, end, duration, reason)
        QMessageBox.information(self, "提示", f"{apply_type}申请提交成功！")
        self.duration.clear()
        self.reason.clear()
        self.load_records()
    
    def load_records(self):
        records = get_adjust_applies(self.user_id)
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(record[3]))
            self.table.setItem(i, 1, QTableWidgetItem(str(record[4])))
            self.table.setItem(i, 2, QTableWidgetItem(str(record[5])))
            self.table.setItem(i, 3, QTableWidgetItem(str(record[6])))
            self.table.setItem(i, 4, QTableWidgetItem(record[7]))
            self.table.setItem(i, 5, QTableWidgetItem(record[8]))

# 考勤确认界面
class ConfirmWidget(QWidget):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 确认表单
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("确认月份:"))
        self.confirm_month = QLineEdit()
        self.confirm_month.setText(datetime.datetime.now().strftime("%Y-%m"))
        form_layout.addWidget(self.confirm_month)
        self.submit_btn = QPushButton("确认考勤")
        self.refresh_btn = QPushButton("刷新")
        form_layout.addWidget(self.submit_btn)
        form_layout.addWidget(self.refresh_btn)
        layout.addLayout(form_layout)
        
        # 确认记录表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["确认月份", "状态", "确认时间"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # 绑定事件
        self.submit_btn.clicked.connect(self.submit_confirm)
        self.refresh_btn.clicked.connect(self.load_records)
        self.load_records()
    
    def submit_confirm(self):
        month = self.confirm_month.text()
        if not month:
            QMessageBox.warning(self, "警告", "请输入确认月份")
            return
        
        add_attendance_confirm(self.user_id, self.user_name, month)
        QMessageBox.information(self, "提示", "考勤确认成功！")
        self.load_records()
    
    def load_records(self):
        records = get_attendance_confirms(self.user_id)
        self.table.setRowCount(len(records))
        for i, record in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(record[3]))
            self.table.setItem(i, 1, QTableWidgetItem(record[4]))
            self.table.setItem(i, 2, QTableWidgetItem(str(record[5]) if record[5] else "-"))

# 登录窗口
class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("用户登录")
        self.setGeometry(300, 300, 400, 200)
        self.user = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 用户名
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名:"))
        self.username = QLineEdit()
        self.username.setText("admin")  # 默认值
        user_layout.addWidget(self.username)
        layout.addLayout(user_layout)
        
        # 密码
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("密码:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setText("admin123")  # 默认值
        pass_layout.addWidget(self.password)
        layout.addLayout(pass_layout)
        
        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)
        
        # 注册按钮
        self.register_btn = QPushButton("注册")
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)
        
        # 忘记密码按钮
        self.forgot_btn = QPushButton("忘记密码")
        self.forgot_btn.clicked.connect(self.forgot_password)
        layout.addWidget(self.forgot_btn)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username.text()
        password = self.password.text()
        user = login_user(username, password)
        if user:
            self.user = user
            self.close()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误")
    
    def register(self):
        # 打开注册对话框
        register_dialog = RegisterDialog(self)
        register_dialog.exec_()
    
    def forgot_password(self):
        # 打开忘记密码对话框
        forgot_dialog = ForgotPasswordDialog(self)
        forgot_dialog.exec_()

# 注册对话框
class RegisterDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("用户注册")
        self.setGeometry(300, 300, 400, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 用户名
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名:"))
        self.username = QLineEdit()
        user_layout.addWidget(self.username)
        layout.addLayout(user_layout)
        
        # 密码
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("密码:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.password)
        layout.addLayout(pass_layout)
        
        # 确认密码
        confirm_layout = QHBoxLayout()
        confirm_layout.addWidget(QLabel("确认密码:"))
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        confirm_layout.addWidget(self.confirm_password)
        layout.addLayout(confirm_layout)
        
        # 姓名
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("姓名:"))
        self.name = QLineEdit()
        name_layout.addWidget(self.name)
        layout.addLayout(name_layout)
        
        # 注册按钮
        self.register_btn = QPushButton("注册")
        self.register_btn.clicked.connect(self.register_user)
        layout.addWidget(self.register_btn)
        
        self.setLayout(layout)
    
    def register_user(self):
        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        name = self.name.text()
        
        # 验证输入
        if not username or not password or not confirm_password or not name:
            QMessageBox.warning(self, "错误", "请填写所有字段")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "错误", "两次输入的密码不一致")
            return
        
        # 检查用户名是否已存在
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        existing = cursor.fetchone()
        conn.close()
        
        if existing:
            QMessageBox.warning(self, "错误", "用户名已存在")
            return
        
        # 创建新用户
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (username, password, name, role) VALUES (?, ?, ?, ?)",
            (username, password, name, "user")  # 默认角色为普通用户
        )
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "成功", "注册成功！")
        self.close()

# 忘记密码对话框
class ForgotPasswordDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("重置密码")
        self.setGeometry(300, 300, 400, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 用户名
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名:"))
        self.username = QLineEdit()
        user_layout.addWidget(self.username)
        layout.addLayout(user_layout)
        
        # 新密码
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("新密码:"))
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.new_password)
        layout.addLayout(pass_layout)
        
        # 确认新密码
        confirm_layout = QHBoxLayout()
        confirm_layout.addWidget(QLabel("确认新密码:"))
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        confirm_layout.addWidget(self.confirm_password)
        layout.addLayout(confirm_layout)
        
        # 重置密码按钮
        self.reset_btn = QPushButton("重置密码")
        self.reset_btn.clicked.connect(self.reset_password)
        layout.addWidget(self.reset_btn)
        
        self.setLayout(layout)
    
    def reset_password(self):
        username = self.username.text()
        new_password = self.new_password.text()
        confirm_password = self.confirm_password.text()
        
        # 验证输入
        if not username or not new_password or not confirm_password:
            QMessageBox.warning(self, "错误", "请填写所有字段")
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "错误", "两次输入的密码不一致")
            return
        
        # 检查用户是否存在
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            QMessageBox.warning(self, "错误", "用户不存在")
            conn.close()
            return
        
        # 更新密码
        cursor.execute(
            "UPDATE user SET password = ? WHERE username = ?",
            (new_password, username)
        )
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "成功", "密码重置成功！")
        self.close()

# 审批管理界面（管理员用）
class ApprovalWidget(QWidget):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 申请类型选择
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("申请类型:"))
        self.apply_type = QComboBox()
        self.apply_type.addItems(["补卡申请", "请假/加班", "调休/出差"])
        self.apply_type.currentIndexChanged.connect(self.load_records)
        type_layout.addWidget(self.apply_type)
        layout.addLayout(type_layout)
        
        # 申请记录表格
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "申请人", "申请类型", "申请内容", "申请时间", "状态", "操作"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_records()
    
    def load_records(self):
        apply_type = self.apply_type.currentText()
        if apply_type == "补卡申请":
            table_name = "supplement_apply"
            records = get_all_applies(table_name)
            self.table.setRowCount(len(records))
            for i, record in enumerate(records):
                self.table.setItem(i, 0, QTableWidgetItem(str(record[0])))
                self.table.setItem(i, 1, QTableWidgetItem(record[2]))
                self.table.setItem(i, 2, QTableWidgetItem("补卡"))
                self.table.setItem(i, 3, QTableWidgetItem(f"{record[3]} {record[4]}: {record[5]}"))
                self.table.setItem(i, 4, QTableWidgetItem(str(record[9])))
                self.table.setItem(i, 5, QTableWidgetItem(record[6]))
                
                # 添加审批按钮
                btn_layout = QHBoxLayout()
                approve_btn = QPushButton("批准")
                approve_btn.clicked.connect(lambda checked, id=record[0]: self.approve_apply(table_name, id))
                reject_btn = QPushButton("拒绝")
                reject_btn.clicked.connect(lambda checked, id=record[0]: self.reject_apply(table_name, id))
                btn_layout.addWidget(approve_btn)
                btn_layout.addWidget(reject_btn)
                
                btn_widget = QWidget()
                btn_widget.setLayout(btn_layout)
                self.table.setCellWidget(i, 6, btn_widget)
        
        elif apply_type == "请假/加班":
            table_name = "leave_apply"
            records = get_all_applies(table_name)
            self.table.setRowCount(len(records))
            for i, record in enumerate(records):
                self.table.setItem(i, 0, QTableWidgetItem(str(record[0])))
                self.table.setItem(i, 1, QTableWidgetItem(record[2]))
                self.table.setItem(i, 2, QTableWidgetItem(record[3]))
                self.table.setItem(i, 3, QTableWidgetItem(f"{record[4]} 至 {record[5]}: {record[7]}"))
                self.table.setItem(i, 4, QTableWidgetItem(str(record[11])))
                self.table.setItem(i, 5, QTableWidgetItem(record[8]))
                
                # 添加审批按钮
                btn_layout = QHBoxLayout()
                approve_btn = QPushButton("批准")
                approve_btn.clicked.connect(lambda checked, id=record[0]: self.approve_apply(table_name, id))
                reject_btn = QPushButton("拒绝")
                reject_btn.clicked.connect(lambda checked, id=record[0]: self.reject_apply(table_name, id))
                btn_layout.addWidget(approve_btn)
                btn_layout.addWidget(reject_btn)
                
                btn_widget = QWidget()
                btn_widget.setLayout(btn_layout)
                self.table.setCellWidget(i, 6, btn_widget)
        
        elif apply_type == "调休/出差":
            table_name = "adjust_apply"
            records = get_all_applies(table_name)
            self.table.setRowCount(len(records))
            for i, record in enumerate(records):
                self.table.setItem(i, 0, QTableWidgetItem(str(record[0])))
                self.table.setItem(i, 1, QTableWidgetItem(record[2]))
                self.table.setItem(i, 2, QTableWidgetItem(record[3]))
                self.table.setItem(i, 3, QTableWidgetItem(f"{record[4]} 至 {record[5]}: {record[7]}"))
                self.table.setItem(i, 4, QTableWidgetItem(str(record[11])))
                self.table.setItem(i, 5, QTableWidgetItem(record[8]))
                
                # 添加审批按钮
                btn_layout = QHBoxLayout()
                approve_btn = QPushButton("批准")
                approve_btn.clicked.connect(lambda checked, id=record[0]: self.approve_apply(table_name, id))
                reject_btn = QPushButton("拒绝")
                reject_btn.clicked.connect(lambda checked, id=record[0]: self.reject_apply(table_name, id))
                btn_layout.addWidget(approve_btn)
                btn_layout.addWidget(reject_btn)
                
                btn_widget = QWidget()
                btn_widget.setLayout(btn_layout)
                self.table.setCellWidget(i, 6, btn_widget)
    
    def approve_apply(self, table_name, apply_id):
        approve_apply(table_name, apply_id, self.user_id)
        QMessageBox.information(self, "提示", "审批成功！")
        self.load_records()
    
    def reject_apply(self, table_name, apply_id):
        reject_apply(table_name, apply_id, self.user_id)
        QMessageBox.information(self, "提示", "审批成功！")
        self.load_records()

# 主窗口
class AttendanceSystem(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user_id = user[0]
        self.user_name = user[2]
        self.user_role = user[3]
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("考勤管理系统")
        self.setGeometry(100, 100, 1000, 600)
        
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标签
        title_label = QLabel(f"欢迎使用考勤管理系统，{self.user_name}！")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # 标签页
        self.tab_widget = QTabWidget()
        
        # 添加各个功能标签
        self.tab_widget.addTab(ClockWidget(self.user_id, self.user_name), "打卡管理")
        self.tab_widget.addTab(SupplementWidget(self.user_id, self.user_name), "补卡申请")
        self.tab_widget.addTab(LeaveWidget(self.user_id, self.user_name), "请假/加班")
        self.tab_widget.addTab(AdjustWidget(self.user_id, self.user_name), "调休/出差")
        self.tab_widget.addTab(ConfirmWidget(self.user_id, self.user_name), "考勤确认")
        
        # 如果是管理员，添加审批管理标签
        if self.user_role == "admin":
            self.tab_widget.addTab(ApprovalWidget(self.user_id, self.user_name), "审批管理")
        
        main_layout.addWidget(self.tab_widget)

# 主程序
if __name__ == "__main__":
    # 初始化数据库
    init_db()
    
    app = QApplication(sys.argv)
    
    # 显示登录窗口
    login_window = LoginWindow()
    login_window.show()
    
    # 等待登录窗口关闭
    app.exec_()
    
    # 如果登录成功，显示主窗口
    if login_window.user:
        main_window = AttendanceSystem(login_window.user)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()
