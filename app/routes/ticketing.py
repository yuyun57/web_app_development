from flask import Blueprint, render_template, request, redirect, url_for

ticketing_bp = Blueprint('ticketing', __name__)

@ticketing_bp.route('/', methods=['GET'])
def index():
    """
    顯示網站首頁與熱門活動列表。
    向 DB 查詢即將開賣或正在販售的 Events 並渲染 templates/index.html。
    """
    pass

@ticketing_bp.route('/concerts/<int:event_id>', methods=['GET'])
def concert_detail(event_id):
    """
    顯示單一活動詳情。
    渲染 templates/concert_detail.html，使用者可點擊搶票按鈕觸發 join_queue。
    """
    pass

@ticketing_bp.route('/concerts/<int:event_id>/seats', methods=['GET'])
def seat_selection(event_id):
    """
    顯示即時座位地圖。
    需確認 Session 是否帶有已通過 Queue 與防黃牛驗證的標記。
    渲染 templates/seat_selection.html。
    """
    pass

@ticketing_bp.route('/concerts/<int:event_id>/seats/lock', methods=['POST'])
def lock_seat(event_id):
    """
    處理座位即時鎖定 (Ajax request)。
    前端點擊座位後發送此請求，後端透過 Redis SETNX 嘗試鎖定該座位，TTL 為 10 分鐘。
    鎖定成功回傳 JSON success 並準備導向結帳頁；失敗則回傳座位已被搶走訊息。
    """
    pass
