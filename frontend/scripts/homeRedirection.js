import { isTokenValid } from "./isTokenValid"


const redirect_path = "./create_user.html"

console.log(token)
try {
  const token = localStorage.getItem("JWToken")
  if (!token || !isTokenValid(token))
    window.location.href = redirect_path
}
catch (e) {
  window.location.href = redirect_path
}
