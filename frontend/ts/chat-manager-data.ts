import Message from "./message-data"
import { sendMessageToServer } from "./connection-manager"

export class ChatData {
  static currentUserId: bigint = BigInt(localStorage.getItem("userId") || -1000)
  static currentUserName: string = localStorage.getItem("username") || "null"
  static chatWindow = document.getElementById("chat-window") as HTMLDivElement
  static sendMessageToBackend: Function = sendMessageToServer

  chatId: bigint
  userIdList: Array<bigint>
  messageList: Array<Message>

  constructor(chatId: bigint, userIdList: Array<bigint>) {
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

