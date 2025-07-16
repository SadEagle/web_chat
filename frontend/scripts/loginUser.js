const loginForm = document.getElementById("loginForm")
const submitForm = document.getElementById("submitForm")

async function loginUser(data) {
  event.preventDefault()

  const formData = new FormData(loginForm, submitForm);
  try {
    response = await fetch("http://localhost:8000/api/user/login_user", {
      method: "POST",
      body: formData,
    });

    const response_data = await response.json()
    if (response.ok) {
      localStorage.setItem("JWToken", response_data);
      localStorage.setItem("username", loginForm.username)
      localStorage.setItem("user_id", loginForm.user_id)
    }
    console.log("JWT token was gotten");
    // Redirect to home
    window.location.replace("./home.html");
  } catch (e) {
    console.error(e);
  }
}

loginForm.addEventListener("submit", loginUser);
