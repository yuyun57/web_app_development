from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/concerts/<int:event_id>/queue/join', methods=['POST'])
def join_queue(event_id):
    """
    處理使用者加入排隊。
    接收 URL 的 event_id，從 session 獲取 user_id，將其推入 Redis 佇列。
    成功後將重導向至等候室狀態頁面 /queue/status。
    """
    pass

@queue_bp.route('/queue/status', methods=['GET'])
def queue_status():
    """
    處理等候室頁面與 polling。
    若帶有 AJAX header，回傳 JSON 等候室進度。
    若為普通 GET 請求，渲染 templates/waiting_room.html 等候室畫面。
    到號後，指引重導向至 /captcha。
    """
    pass

@queue_bp.route('/captcha', methods=['GET'])
def captcha_page():
    """
    顯示防黃牛驗證頁面。
    條件是必須已到號才能進入。
    渲染 templates/captcha.html 表單。
    """
    pass

@queue_bp.route('/captcha/verify', methods=['POST'])
def verify_captcha():
    """
    處理防黃牛驗證提交。
    接收使用者的答題或拼圖參數，驗證成功後給予選位 token 標籤（寫入 session），
    並導向對應的 /concerts/<id>/seats。
    """
    pass
