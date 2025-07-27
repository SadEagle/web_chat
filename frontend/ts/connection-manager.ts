import { Message } from "./data-model";

export async function sendMessageToServer(message: Message) {
  const sendMessageResponse = await fetch('/api/chat/send_message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(message)
  });

  if (!sendMessageResponse.ok) {
    if (sendMessageResponse.status === 404) {
      throw new Error("Wrong endpoint, recheck request url")
    }
  }

  const data = await sendMessageResponse.json();
  console.log('Message sent:', data);
}

export async function getBatchMessageFromServer() { }

// Work with users id list that may be lenght 1
export async function getUsersInfoFromServer() { }

export async function getChatUsersIdFromServer() { }

// Think that structure that getting id's and later send extra query is prefferable because of valkey non-message correlated data
// At least users will 100% be valkey, will chats also be the same - questionable, but possible
export async function getUserChatsIdFromServer() { }

export async function getChatsInfoFromServer() { }
