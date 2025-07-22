const loginForm = document.getElementById("loginForm") as HTMLFormElement
// Not sure
const submitForm = document.getElementById("login-submit-form") as HTMLButtonElement

async function loginUser(event: Event) {
  event.preventDefault()

  const formData = new FormData(loginForm, submitForm);
  try {
    const response = await fetch("/api/user/login_user", {
      method: "POST",
      body: formData,
    });

    const responseData = await response.json()
    if (response.ok) {
      localStorage.setItem("JWToken", responseData);
      localStorage.setItem("username", loginForm.username)
      localStorage.setItem("userId", loginForm.userId)
    }
    console.log("JWT token was gotten");
    // Redirect to home
    window.location.replace("/home.html");
  } catch (e) {
    console.error(e);
    // TODO: add error message over form
  }
}

loginForm.addEventListener("submit", loginUser);
