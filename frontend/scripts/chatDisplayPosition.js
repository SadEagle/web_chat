const scrollContainer = document.getElementById('display_chat_box');
function scrollToBottom() {
  // const scrollContainer = document.querySelector('.chat_display_scroll_container');
  scrollContainer.scrollTop = scrollContainer.scrollHeight;
}

window.addEventListener('DOMContentLoaded', scrollToBottom);
// New message drop chat to the bottom
document.getElementById('send_message_button').addEventListener('click', () => {
  setTimeout(scrollToBottom, 0);
});
