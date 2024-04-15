const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault(); //submit 했을 때 자동 새로고침 막기

  const body = new FormData(form);
  //세계시간 기준으로 보냄
  body.append("insertAt", new Date().getTime());

  try {
    const res = await fetch("/items", {
      method: "POST",
      body, //body: body 를 줄여서 쓸 수 있음
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
