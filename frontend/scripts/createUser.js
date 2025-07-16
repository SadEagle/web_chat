const createUserForm = document.getElementById("createUserForm")

async function updateUser(data) {
  event.preventDefault()

  const formData = new FormData(createUserForm);
  try {
    response = await fetch("http://localhost:8000/api/user/create_user", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    });

    const response_data = await response.json()
    if (response.status == 201)
      console.log("Sucsessuffly create user ${formData.login}");
    // Redirect to login
    window.location.replace("./login.html");
  } catch (e) {
    console.error(e);
  }
}

createUserForm.addEventListener("submit", updateUser);
