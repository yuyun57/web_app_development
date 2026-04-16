from flask import Blueprint, render_template, request, redirect, url_for, session

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/checkout', methods=['GET'])
def checkout():
    """
    顯示訂單結帳頁面。
    從 Redis 取得該使用者目前已鎖定保留的位子與金額。
    渲染 templates/checkout.html。
    """
    pass

@payment_bp.route('/orders', methods=['POST'])
def create_order():
    """
    處理訂單生成與金流結帳。
    確認 Redis 中的 10 分鐘保留鎖定是否有效，若有效則將記錄寫入 DB Order 表，並把 Seat 改為 SOLD。
    最後提早刪除 Redis Lock。成功後導向 /orders/<order_id>。
    """
    pass

@payment_bp.route('/orders/<int:order_id>', methods=['GET'])
def order_detail(order_id):
    """
    顯示歷史訂單詳情與票券狀態。
    查詢 Order 及其關聯的 Seat、Event。
    渲染 templates/order_detail.html。
    """
    pass
