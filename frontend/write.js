const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault(); //submit 했을 때 자동 새로고침 막기

  try {
    const res = await fetch("/items", {
      method: "POST",
      body: new FormData(form),
    });

    const data = await res.json(); // 응답을 데이터로 바꾸기

    //서버에서 내려주기로 한 200이면 메인페이지로 이동 실행
    if (data === "200") {
      window.location.pathname = "/";
      console.log("완료");
    }
  } catch (e) {
    console.error(e); //에러 출력
  }
};

form.addEventListener("submit", handleSubmitForm);
