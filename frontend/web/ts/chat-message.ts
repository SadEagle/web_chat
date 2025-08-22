import { ChatData } from "./chat-manager-data.js";
import { Message } from "./data-model.js";

const messageArea = document.getElementById("message-area") as HTMLTextAreaElement
const sendMessageButton = document.getElementById("send-message-button") as HTMLButtonElement
// WARN: dummy params
const USER_ID: string = localStorage.getItem("userId") || "null"
const CHAT_ID: string = "1"
const USER_ID_LIST: Array<string> = []

const currentChat = new ChatData(CHAT_ID, USER_ID_LIST)

function sendMessage() {
  console.log(`Current user id ${USER_ID}`)
  if (!messageArea.value) {
    messageArea.value = "";
    return;
  }
  let messageInfo = new Message(CHAT_ID, USER_ID, messageArea.value)
  currentChat.addMessage(messageInfo)
  messageArea.value = "";
}

sendMessageButton.addEventListener("click", sendMessage)
// document.addEventListener("keypress", function(event) {
//   if (document.activeElement === messageArea && event.key == "Enter" && event.altKey) {
//     event.preventDefault()
//     sendMessage()
//   }
// });
