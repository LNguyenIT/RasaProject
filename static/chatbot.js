// Hàm gửi tin nhắn
function sendMessage() {
    var input = document.getElementById("user-input").value;
    if (input) {
        var chatBox = document.getElementById("chat-box");
        var userMessage = document.createElement("div");
        userMessage.classList.add("message", "user-message");
        userMessage.innerText = "Bạn: " + input;
        chatBox.appendChild(userMessage);

        // Lấy phản hồi từ chatbot
        fetch(`/chatbot_response?message=${input}`)
            .then(response => response.json())
            .then(data => {
                var botMessage = document.createElement("div");
                botMessage.classList.add("message", "bot-message");
                botMessage.innerText = "Bot: " + data.response;
                chatBox.appendChild(botMessage);

                // Scroll to bottom
                chatBox.scrollTop = chatBox.scrollHeight;
            });

        // Clear input field
        document.getElementById("user-input").value = '';
    }
}

// Bắt sự kiện khi người dùng nhấn phím Enter
document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Ngăn không cho nhập thêm dòng mới khi nhấn Enter
        sendMessage(); // Gọi hàm gửi tin nhắn
    }
});
