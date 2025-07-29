let scrollContainer = document.getElementById('display-chat-box') as HTMLDivElement
let sendMessageButton = document.getElementById("send-message-button") as HTMLButtonElement

function scrollToBottom() {
  // const scrollContainer = document.querySelector('.chat-display-scroll-container');
  scrollContainer.scrollTop = scrollContainer.scrollHeight;
}

window.addEventListener('DOMContentLoaded', scrollToBottom);
// New message drop chat to the bottom
sendMessageButton.addEventListener('click', () => {
  setTimeout(scrollToBottom, 0);
});
