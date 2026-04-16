from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入與註冊。
    GET: 渲染 templates/login.html 頁面。
    POST: 接收 phone 與 password，查驗 User Model 密碼是否吻合。若未註冊則建立新 User 並寫入 Session，成功後導向 /verify。
    """
    if request.method == 'POST':
        pass
    return render_template('login.html')

@auth_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    """
    處理實名驗證。
    GET: 渲染 templates/verify.html 頁面。
    POST: 接收表單傳來的 id_card_number，確認是否已綁定。若無則更新 User 資料並重導向至首頁。
    """
    if request.method == 'POST':
        pass
    return render_template('verify.html')
