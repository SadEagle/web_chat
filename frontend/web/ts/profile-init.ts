/**
 * @module Get all essential metedata by it's token
 */

import { User } from "./data-model"

function redirectToLogin() {
  window.location.replace("/login")
}

async function loadUserProfile() {
  const token = localStorage.getItem("JWToken")
  if (!token) {
    redirectToLogin()
    console.log("Token wasn't found")
    return
  }
  // TODO: add token expiration check

  // Get user profile
  const userResponse = await fetch('/api/user/get_current_user', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  })
  if (!userResponse.ok) {
    if (userResponse.status === 404) {
      throw new Error("Wrong endpoint, recheck request url")
    }
    else {
      redirectToLogin()
      throw new Error("Wrong user token or user was deleted after token was granted but token isn't expired")
    }
  }
  const user: User = await userResponse.json()
  localStorage.setItem("username", user.login)
  localStorage.setItem("userId", user.user_id.toString())
  // Get user chats ids
  const chatIdArrayResponse = await fetch('/api/chat/get_current_user_chat_ids', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  })
  if (!chatIdArrayResponse.ok) {
    if (chatIdArrayResponse.status === 404) {
      throw new Error("Wrong endpoint, recheck request url")
    }
  }
  const chatIdArray: Array<string> = await chatIdArrayResponse.json()

  localStorage.setItem("chatIdArray", JSON.stringify(chatIdArray))
  // TODO: make 2 options below as isolated functions
  // 1. Get full chat data
  // 2. Visualise data itself
}

loadUserProfile()
// document.addEventListener('DOMContentLoaded', loadUserProfile)
