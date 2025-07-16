const chatWindow = document.getElementById("chat_window")
const messageArea = document.getElementById("message_area")
const sendMessageButton = document.getElementById("send_message_button")


const CHAT_ID = 1
const USER_ID = localStorage.getItem("user_id")
const USERNAME = localStorage.getItem("username")

class Message {
  owner_user_id = localStorage.getItem("user_id")
  constructor(chat_id, user_id, message) {
    this.chat_id = chat_id
    this.user_id = user_id
    this.messageData = message
    this.is_owner_message = this.owner_user_id == user_id
  }
}

class ChatData {
  messageList = []
  addMessage(message) {
    if (!message.messageData) {
      // Skip if message empty
      return;
    }
    this.messageList.push(message)
    this.visualizeMessage(message)

    // TODO: Add back-end send
    // this.sendMessageToBackend(message);
  }

  visualizeMessage(message) {
    let messageClass = message.is_owner_message ? "my_message" : "stranger_message"
    let messageElement = document.createElement("div");
    messageElement.classList.add(messageClass)
    messageElement.textContent = message.messageData;
    chatWindow.appendChild(messageElement)
  }

  visualizeFullChat() {
    chatWindow.innerHTML = "";
    for (messageSample in this.messageList) {
      this.visualizeMessage(messageSample)
    }
  }

  // TODO: check ai function
  async sendMessageToBackend(message) {
    try {
      const response = await fetch('http://localhost:8000/api/chat/send_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(message)
      });
      const data = await response.json();
      console.log('Message sent:', data);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }
}


const currentChat = new ChatData()

function send_message() {
  event.preventDefault()
  message_text = messageArea.value
  message_info = new Message(CHAT_ID, USER_ID, message_text)
  currentChat.addMessage(message_info)
  messageArea.value = "";
}

sendMessageButton.addEventListener("click", send_message)
