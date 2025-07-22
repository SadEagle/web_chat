import { ChatData } from "./chat-manager-data";
import Message from "./message-data";

// WARN: dummy params
const USER_ID: bigint = BigInt(1)
const CHAT_ID: bigint = BigInt(1)
const USER_ID_LIST: Array<bigint> = []

const messageArea = document.getElementById("message-area") as HTMLTextAreaElement
const currentChat = new ChatData(CHAT_ID, USER_ID_LIST)

function sendMessage() {
  if (!messageArea.value) {
    messageArea.value = "";
    return;
  }
  let messageInfo = new Message(CHAT_ID, USER_ID, messageArea.value)
  currentChat.addMessage(messageInfo)
  messageArea.value = "";
}

sendMessageButton.addEventListener("click", sendMessage)

document.addEventListener("keypress", function(event) {
  event.preventDefault()
  if (event.key == "Enter") {
    sendMessage()
  }
});
