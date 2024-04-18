const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256PW = sha256(formData.get("password"));
  formData.set("password", sha256PW);

  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });

  const data = await res.json();

  console.log(data);

  if (res.status === 200) {
    alert("로그인 성공");
    window.location.pathname = "/";
  } else if (res.status === 401) {
    alert("ID 혹은 PW가 틀렸습니다");
  }
};

form.addEventListener("submit", handleSubmit);
