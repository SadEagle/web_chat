const createUserForm = document.getElementById("create-user-form") as HTMLFormElement

async function updateUser(event: Event) {
  event.preventDefault()

  const formData = new FormData(createUserForm);
  const createUserResponse = await fetch("/api/user/create_user", {
    method: "POST",
    body: JSON.stringify(Object.fromEntries(formData)),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  });
  if (!createUserResponse.ok) {
    if (createUserResponse.status === 404) {
      throw new Error("Wrong endpoint, recheck request url")
    }
    else if (createUserResponse.status === 422) {
      throw new Error("Bad field data")
    }
    else {
      throw new Error("Unexpected error")
    }
  }
  else {
    console.log(`Sucsessuffly create user ${formData.get("login")}. Redirect to /login`)
    window.location.href = "/login"
  }
}

createUserForm.addEventListener("submit", updateUser)
