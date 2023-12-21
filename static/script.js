const messageBar = document.querySelector(".bar-wrapper input");
const sendBtn = document.querySelector(".bar-wrapper button");
const messageBox = document.querySelector(".message-box");

function sendMessage() {
    if (messageBar.value.length > 0) {
        const isScrolledToBottom = messageBox.scrollHeight - messageBox.clientHeight <= messageBox.scrollTop + 1;
        const UserTypedMessage = messageBar.value;
        messageBar.value = "";

        let message =
            `<div class="chat message">
            <span class="material-symbols-outlined">
            person
            </span>
            <span>
            ${UserTypedMessage}
            </span>
        </div>`;

        let response =
            `<div class="chat response">
            <span class="material-symbols-outlined">
            support_agent
            </span>
            <span class="new">...</span> <!-- Aqui estava o ponto de suspensão -->

        </div>`;

        messageBox.insertAdjacentHTML("beforeend", message);

        setTimeout(() => {
            messageBox.insertAdjacentHTML("beforeend", response);
    
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "user_message": UserTypedMessage  // Envia a mensagem do usuário para o backend
                })
            }
    
            fetch('/chatbot', requestOptions) // Envia a solicitação para a rota Flask '/chatbot'
                .then(res => res.json())
                .then(data => {
                    const ChatBotResponse = document.querySelector(".response .new");
                    ChatBotResponse.innerHTML = data.response; // Define a resposta do chatbot do backend
                    ChatBotResponse.classList.remove("new");
                })
                .catch((error) => {
                    ChatBotResponse.innerHTML = "Oops! An error occurred. Please try again."
                })
                
            if (isScrolledToBottom) {
                messageBox.scrollTop = messageBox.scrollHeight - messageBox.clientHeight;
            }
        }, 100);
        
    }
}


messageBar.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);