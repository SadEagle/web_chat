import { isTokenValid } from "./is-token-valid"

const redirectPath = "/login.html"

function checkToken(): void {
  try {
    const token = localStorage.getItem("JWToken")
    if (!token || !isTokenValid(token)) {
      console.log("JWToken is outdated")
      window.location.href = redirectPath
    }
  }
  catch (e) {
    console.log("JWToken wasn't found")
    window.location.href = redirectPath
  }
}

checkToken()
