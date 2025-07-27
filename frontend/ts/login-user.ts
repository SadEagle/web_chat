const loginForm = document.getElementById("loginForm") as HTMLFormElement
// Not sure
const submitForm = document.getElementById("login-submit-form") as HTMLButtonElement

async function loginUser(event: Event) {
  event.preventDefault()

  const formData = new FormData(loginForm, submitForm);
  const response = await fetch("/api/user/login_user", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Wrong endpoint, recheck request url")
    }
    else {
      console.log("Login unsuccessfull. Try again.")
    }
  }

  const responseData = await response.json()
  localStorage.setItem("JWToken", responseData.access_token)
  console.log("Login successfull. Token was gained.");
  window.location.replace("/home");
}

loginForm.addEventListener("submit", loginUser);
