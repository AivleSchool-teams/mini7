const nav = document.querySelector(".mobile_nav_list");
const burger = document.querySelector(".nav_burger");

burger.addEventListener("click", () => {
  nav.classList.toggle("show_mobile_nav");
});

var fileNames = [];

function loadFile(input) {
  // 모든 선택된 파일의 이름 추가
  for (let i = 0; i < input.files.length; i++) {
      fileNames.push(input.files[i].name);
  }

  // 파일 목록 표시 업데이트
  updateFileDisplay();
}

function updateFileDisplay() {
    var displayNames;

    // 파일이 3개 이상인 경우, 처음 3개의 이름만 표시하고 "..." 추가
    if (fileNames.length > 3) {
        displayNames = fileNames.slice(0, 3).join(", ") + ", ...";
    } else {
        displayNames = fileNames.join(", ");
    }

    // 표시할 파일 이름을 HTML 요소에 설정
    document.getElementById("fileName").textContent = displayNames;
}