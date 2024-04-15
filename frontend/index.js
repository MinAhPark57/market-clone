const renderData = (data) => {
  //[{id:1, title:'팝니다', description:'상태 좋아요'},{id:2, title : '   ' ,description:'  '}....]

  const main = document.querySelector("main");

  data.forEach((obj) => {
    const div = document.createElement("div");
    div.innerText = obj.title;
    main.appendChild(div);
  });
};

const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  renderData(data);
};

fetchList();
