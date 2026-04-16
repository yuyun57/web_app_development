# 路由設計文件 (API & Routes Design)

根據本專案的架構設計 (ARCHITECTRUE.md)、流程圖 (FLOWCHART.md) 與資料庫設計 (DB_DESIGN.md)，本文件統整並規劃了所有 Flask 藍圖 (Blueprints) 的路由與對應邏輯。

## 1. 路由總覽表格

| 模組 | 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ticketing** |網站首頁 | GET | / | templates/index.html | 顯示近期演唱會列表 |
| **ticketing** |演唱會詳情 | GET | /concerts/<id> | templates/concert_detail.html | 顯示場次資訊、票價、開賣時間 |
| **auth** |登入/註冊頁面 | GET | /login | templates/login.html | 輸入手機與密碼介面 |
| **auth** |處理使用者登入 | POST | /login | — | 驗證帳密並寫入 Session |
| **auth** |實名制驗證頁面 | GET | /verify | templates/verify.html | 輸入身分證實名認證 |
| **auth** |提交實名驗證 | POST | /verify | — | 更新資料庫中 `id_card_number` |
| **queue** |加入搶票排隊 | POST | /concerts/<id>/queue/join| — | 將 User 丟進 Redis 佇列，導向等候室 |
| **queue** |排隊狀態與輪詢 | GET | /queue/status | templates/waiting_room.html| 等候室頁面，JS 將根據此路由 polling|
| **queue** |防黃牛驗證頁面 | GET | /captcha | templates/captcha.html | 到號時，填寫問答驗證 |
| **queue** |提交防黃牛解答 | POST | /captcha/verify | — | 驗證通過即給予選位權限 token |
| **ticketing** |可視化座位地圖 | GET | /concerts/<id>/seats | templates/seat_selection.html| 顯示該場次剩餘可選座位 |
| **ticketing** |點選並鎖定座位 | POST | /concerts/<id>/seats/lock| — | 設定 Redis 分散式鎖，成功導向結帳 |
| **payment** |結帳與確認頁面 | GET | /checkout | templates/checkout.html | 確認欲購座位資訊、付款選擇 |
| **payment** |提交付款與訂單 | POST | /orders | — | 正式結帳並將 Order 寫入 SQLite |
| **payment** |查詢歷史訂單 | GET | /orders/<id> | templates/order_detail.html | 顯示該筆訂單與票券狀態 |

---

## 2. 每個路由的詳細說明

### 模組：`auth.py`
* **POST `/login`**
  * **輸入**：表單 `phone`, `password`
  * **處理邏輯**：查驗 User Model 密碼是否吻合。若該手機未註冊則建立新 User。寫入 Session。
  * **輸出**：重導向至 `/verify` 或 首頁。
* **POST `/verify`**
  * **輸入**：表單 `id_card_number`
  * **處理邏輯**：確認該實名證件是否已被綁定，若無則更新該 User 的實名認證欄位。
  * **輸出**：重導向至首頁的演唱會清單。

### 模組：`queue.py`
* **POST `/concerts/<id>/queue/join`**
  * **輸入**：URL 路徑的 `<id>` (對應 `event_id`)，以及使用者的 Session。
  * **處理邏輯**：呼叫 Redis Service，以當前 Timestamp 為分數寫入 Sorted Set。
  * **輸出**：重導向至 `/queue/status?event_id=<id>`。
* **GET `/queue/status`**
  * **處理邏輯**：查詢 Redis Queue 目前的順位與進度。
  * **輸出**：若已到號則重導向 `/captcha`，若未到號則渲染 `waiting_room.html`。
* **POST `/captcha/verify`**
  * **輸入**：表單的回答。
  * **處理邏輯**：驗證碼邏輯驗證，成功則給 Session tag。
  * **輸出**：重導向至 `/concerts/<id>/seats`。

### 模組：`ticketing.py`
* **GET `/concerts/<id>/seats`**
  * **處理邏輯**：查詢 `Seat` 表與目前存在 Redis 中被鎖定的座位，準備渲染空位地圖。
  * **輸出**：渲染 `seat_selection.html`。
* **POST `/concerts/<id>/seats/lock`**
  * **輸入**：AJAX 傳入 `seat_number`
  * **處理邏輯**：對 Redis 執行 `SETNX` 加上長度為 600 秒的 TTL 時間過期鎖。
  * **輸出**：成功回傳 HTTP 200 (前端跳轉 `/checkout`)；失敗回傳 HTTP 409 Conflict。

### 模組：`payment.py`
* **POST `/orders`**
  * **輸入**：表單中的 `seat_id`, `payment_method`
  * **處理邏輯**：確認 Redis 在 10 分鐘內鎖是否仍有效。建立 `Order` 資料庫紀錄 (`status='PAID'`)。更新 `Seat.status = 'SOLD'`，提早釋放 Redis 鎖定。
  * **輸出**：重導向至 `/orders/<id>`。

---

## 3. Jinja2 模板清單

所有的模板檔案應放在 `app/templates/` 且繼承自 `base.html`，以達到一致的 UI 風格。

1. **`base.html`**：包含 Navbar (回到首頁、我的訂單、會員登入/登出狀態)、Footer、CSS 引入。
2. **`index.html`**：(繼承 base.html) 首頁，卡片式呈現 `events`。
3. **`concert_detail.html`**：(繼承 base.html) 單場演唱會細節與大顆的「立即搶票」按鈕。
4. **`login.html`**：(繼承 base.html) 登入/註冊表單。
5. **`verify.html`**：(繼承 base.html) 實名制輸入表單。
6. **`waiting_room.html`**：(不繼承/簡化 base.html) 極簡畫面的虛擬等候室，有 Loader 與 JS 倒數順位。
7. **`captcha.html`**：(簡化 base.html) 防黃牛驗證表單。
8. **`seat_selection.html`**：(繼承 base.html) 包含圖形化座位網格與 JavaScript 即時鎖定邏輯。
9. **`checkout.html`**：(繼承 base.html) 訂單資訊呈現單與付款流程。
10. **`order_detail.html`**：(繼承 base.html) 電子票券與付款成功畫面。
