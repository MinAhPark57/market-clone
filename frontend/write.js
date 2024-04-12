const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault(); //submit 했을 때 자동 새로고침 막기
  await fetch("/items", {
    method: "POST",
    body: new FormData(form),
  });
  console.log("제출완료");
};

form.addEventListener("submit", handleSubmitForm);
