export default class Message {
  // FIX:: we need to read userId 100%
  static currentUserId: bigint = BigInt(localStorage.getItem("userId") || "-1000")

  chatId: bigint
  userId: bigint
  messageData: string
  isOwnerMessage: boolean

  constructor(chatId: bigint, userId: bigint, message: string) {
    this.chatId = chatId
    this.userId = userId
    this.messageData = message
    this.isOwnerMessage = userId === Message.currentUserId
  }
}

