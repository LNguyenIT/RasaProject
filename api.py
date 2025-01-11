from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Dữ liệu giả lập cho đơn hàng và sản phẩm
orders_status_data = {
    "1001": "Đang vận chuyển",
    "1002": "Đã giao hàng",
    "1003": "Hủy đơn",
}

# Dữ liệu sản phẩm và trạng thái
products_status_data = {
    "Samsung Galaxy S22": "Còn hàng",
    "Iphone 15 Pro max": "Còn hàng",
    "Xiaomi 13T": "Hết hàng",
}

# Dữ liệu bảo hành
warranty_data = {
    "Samsung Galaxy S22": {"2025-12-01": "12 tháng"},
    "Iphone 15 Pro max": {"2024-06-01": "12 tháng"},
    "Xiaomi 13T": {"2026-02-01": "24 tháng"},
}


# Trang chủ để hiển thị giao diện chat
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatbot_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.json.get("message")
    if not user_message:  # Nếu không có thông điệp từ người dùng, gửi câu chào hỏi
        response = "Chào bạn! Tôi giúp được gì cho bạn?"
    else:
        response = get_response_from_rasa(user_message)  # Gửi thông điệp này đến chatbot (Rasa) và lấy phản hồi
    return jsonify({"response": response})


RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"


def get_response_from_rasa(user_message):
    payload = {"sender": "user", "message": user_message}

    # Gửi yêu cầu POST tới Rasa
    response = requests.post(RASA_API_URL, json=payload)

    try:
        rasa_response = response.json()
        # In ra toàn bộ phản hồi từ Rasa
        print("Response từ Rasa:", json.dumps(rasa_response, indent=2))  # In dữ liệu JSON đẹp

        if rasa_response:
            # Trả về văn bản từ Rasa (nếu có)
            return rasa_response[0].get("text", "Xin lỗi, tôi không hiểu yêu cầu của bạn.")
        else:
            return "Có lỗi xảy ra khi kết nối đến chatbot."
    except ValueError:
        # Xử lý nếu phản hồi không phải là JSON hợp lệ
        return "Không thể nhận phản hồi hợp lệ từ Rasa."


# Cung cấp thông tin khuyến mãi qua API
@app.route('/promotion_info', methods=['GET'])
def promotion_info():
    promotion_url = "https://ems.vlute.edu.vn/"
    promotion_info = "Hiện tại đang có chương trình giảm giá đặc biệt 20% cho các sản phẩm điện thoại Samsung!"
    return jsonify({
        'promotion_url': promotion_url,
        'promotion_info': promotion_info
    })


if __name__ == '__main__':
    app.run(debug=True)