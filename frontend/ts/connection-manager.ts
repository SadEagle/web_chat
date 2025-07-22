import Message from "./message-data";

export async function sendMessageToServer(message: Message) {
  try {
    const response = await fetch('/api/chat/send_message', {
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

export async function getBatchMessageFromServer() { }

// Work with users id list that may be lenght 1
export async function getUsersInfoFromServer() { }

export async function getChatUsersIdFromServer() { }

// Think that structure that getting id's and later send extra query is prefferable because of valkey non-message correlated data
// At least users will 100% be valkey, will chats also be the same - questionable, but possible
export async function getUserChatsIdFromServer() { }

export async function getChatsInfoFromServer() { }
