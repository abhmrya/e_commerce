  const toggleBtn = document.getElementById('toggleBtn');
  const switchText = document.getElementById('switch-text');
  const switchDesc = document.getElementById('switch-desc');
  const loginFormDiv = document.querySelector('.login-form');
  const registerFormDiv = document.querySelector('.signup-form');

  toggleBtn.addEventListener('click', () => {
    const isLoginShown = loginFormDiv.classList.contains('block');
    if (isLoginShown) {
      loginFormDiv.classList.replace('block', 'hidden');
      registerFormDiv.classList.replace('hidden', 'block');
      toggleBtn.textContent = "Login";
      switchText.textContent = "Already a member?";
      switchDesc.textContent = "Click below to log into your account.";
    } else {
      loginFormDiv.classList.replace('hidden', 'block');
      registerFormDiv.classList.replace('block', 'hidden');
      toggleBtn.textContent = "Register";
      switchText.textContent = "New here?";
      switchDesc.textContent = "Click below to create an account.";
    }
  });

  // REGISTER FORM SUBMIT
  document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = {
      first_name: form.first_name.value,
      last_name: form.last_name.value,
      username: form.username.value,
      email: form.email.value,
      password: form.password.value
    };

    const res = await fetch("/api/apiregister/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const resData = await res.json();
    if (res.ok) {
      document.getElementById("registerSuccess").classList.remove("hidden");
      document.getElementById("registerError").classList.add("hidden");
      form.reset();
    } else {
      document.getElementById("registerError").textContent = resData?.detail || Object.values(resData).join(" ");
      document.getElementById("registerError").classList.remove("hidden");
      document.getElementById("registerSuccess").classList.add("hidden");
    }
  });

  // LOGIN FORM SUBMIT
  document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = {
      username: form.username.value,
      password: form.password.value
    };

    const res = await fetch("/api/apilogin/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const resData = await res.json();
    if (res.ok) {
      // Save token to localStorage
      localStorage.setItem("access", resData.tokens.access);
      localStorage.setItem("refresh", resData.tokens.refresh);
      alert("Login successful!");
      window.location.href = "index.html"; // or wherever you want
    } else {
      document.getElementById("loginError").textContent = resData?.detail || "Invalid login";
      document.getElementById("loginError").classList.remove("hidden");
    }
  });