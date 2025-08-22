import { Message } from "./data-model.js"
import { sendMessageToServer } from "./connection-manager.js"

export class ChatData {
  static currentUserId: string = localStorage.getItem("userId") || "null"
  static currentUserName: string = localStorage.getItem("username") || "null"
  static chatWindow = document.getElementById("chat-window") as HTMLDivElement
  static sendMessageToBackend: Function = sendMessageToServer

  chatId: string
  userIdList: Array<string>
  messageList: Array<Message>

  constructor(chatId: string, userIdList: Array<string>) {
    this.chatId = chatId
    this.userIdList = userIdList
    this.messageList = []
  }

  addMessage(message: Message): void {
    if (!message.messageData) {
      // Skip if message empty
      return;
    }
    this.messageList.push(message)
    this.visualizeMessage(message)

    ChatData.sendMessageToBackend(message);
  }

  visualizeMessage(message: Message): void {
    let messageClass = message.isOwnerMessage ? "my-message" : "stranger-message"
    let messageElement = document.createElement("div");
    messageElement.classList.add(messageClass)
    messageElement.textContent = message.messageData;
    ChatData.chatWindow.appendChild(messageElement)
  }

  visualizeFullChat() {
    ChatData.chatWindow.innerHTML = "";
    for (let messageSample of this.messageList) {
      this.visualizeMessage(messageSample)
    }
  }
}
