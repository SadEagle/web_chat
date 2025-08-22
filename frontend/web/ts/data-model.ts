export type User = {
  user_id: string
  login: string

};

export type Chat = {
  id: string
  name: string
  user_id_list: Array<string>
};



export class Message {
  // FIX:: we need to read userId 100%
  static currentUserId: string = localStorage.getItem("userId") || "null"

  chatId: string
  userId: string
  messageData: string
  isOwnerMessage: boolean

  constructor(chatId: string, userId: string, message: string) {
    this.chatId = chatId
    this.userId = userId
    this.messageData = message
    this.isOwnerMessage = userId === Message.currentUserId
  }
}
