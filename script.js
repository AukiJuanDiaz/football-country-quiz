const clubs = ["Real Madrid", "Barcelona", "Bayern Munich", "Manchester United", "Chelsea", "PSG", "Liverpool"];

const input = document.querySelector("#club-input");
const list = document.querySelector("#club-list");

input.addEventListener("input", () => {
  const matches = clubs.filter(club => club.toLowerCase().startsWith(input.value.toLowerCase()));
  
  list.innerHTML = "";
  matches.forEach(match => {
    const item = document.createElement("div");
    item.textContent = match;
    item.addEventListener("click", () => {
      input.value = match;
      list.innerHTML = "";
    });
    list.appendChild(item);
  });
});