const createUserForm = document.getElementById("create-user-form") as HTMLFormElement

async function updateUser(event: Event) {
  event.preventDefault()

  const formData = new FormData(createUserForm);
  try {
    const response = await fetch("/api/user/create_user", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    });
    if (response.status == 201) {
      console.log(`Sucsessuffly create user ${formData.get("login")}`);
      // Redirect to login
      window.location.replace("/login.html");
    }
  } catch (e) {
    console.error(e);
  }
}

createUserForm.addEventListener("submit", updateUser);
