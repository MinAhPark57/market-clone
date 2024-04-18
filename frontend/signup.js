const form = document.querySelector("#signup-form");

const checkPW = () => {
  const formData = new FormData(form);
  const PW1 = formData.get("password");
  const PW2 = formData.get("password2");

  if (PW1 === PW2) {
    return true;
  } else return false;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256PW = sha256(formData.get("password"));
  formData.set("password", sha256PW);

  const div = document.querySelector("#info");

  if (checkPW()) {
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });
    const data = await res.json();

    //서버에서 성공 메시지 받았을때만 표시
    if (data === "200") {
      div.innerText = "회원가입 성공";
      div.style.color = "blue";
    }
  } else {
    div.innerText = "비밀번호가 같지 않습니다!";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
