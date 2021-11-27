var gameover = false;
// Listening to key press
addEvent(document, "keypress", function (e) {
  e = e || window.event;
  if (
    e.key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] &&
    !gameover
  ) {
    updateCell(e.key);
  }
});

function addEvent(element, eventName, callback) {
  if (element.addEventListener) {
    element.addEventListener(eventName, callback, false);
  } else if (element.attachEvent) {
    element.attachEvent("on" + eventName, callback);
  } else {
    element["on" + eventName] = callback;
  }
}

//  Customize add focus class during animation

const addFocusOnAnimation = (val, i) => {
  // remove focus from all the cells that already have it
  for (let i = 0; i < cells.length; i++) {
    cells[i].classList.remove("focus");
    cells[i].classList.remove("secondary-focus");
    if (
      cells[i].innerHTML.trim() === val.toString() &&
      cells[i].innerHTML.trim() !== "0"
    ) {
      cells[i].classList.add("secondary-focus");
    }
  }
  cells[i].classList.remove("secondary-focus");
  cells[i].classList.add("focus");
};

// add focus class to a cell element when it is been clicked
const addFocus = (e) => {
  // remove focus from all the cells that already have it
  if (gameover) {
    return null;
  }
  for (let i = 0; i < cells.length; i++) {
    cells[i].classList.remove("focus");
    cells[i].classList.remove("secondary-focus");
    if (
      cells[i].innerHTML.trim() === e.target.innerHTML.trim() &&
      +cells[i].innerHTML.trim() !== 0
    ) {
      cells[i].classList.add("secondary-focus");
    }
  }
  e.target.classList.remove("secondary-focus");
  e.target.classList.add("focus");
};

cells = document.querySelectorAll("div.cell");
subcells =  document.querySelectorAll("div.sub-cell")

cells.forEach((cell) => {
  cell.addEventListener("click", addFocus);
});

subcells.forEach((cell) => {
  cell.addEventListener("click", () => updateCell(cell.innerHTML.trim()))
})

//  Update the grid in the backend and the frontend with the new information of a particular cell
const update = async (val, row_index, col_index, i = 0, fnc = () => {}) => {
  fnc(val, i);
  if (gameover) {
    return null;
  }
  const response = await fetch("http://127.0.0.1:5000", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      val: val,
      row: row_index,
      col: col_index,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data["editable"] && !data["solved"]) {
        cells[i].innerHTML = data["val"];
        for (let i = 0; i < data["cellsStatus"].length; i++) {
          // console.log(cells[i].innerHTML.trim(), typeof(cells[i].innerHTML.trim()));
          if (data["cellsStatus"][i] && data["listOfEditable"][i] && cells[i].innerHTML.trim() !== "0") {
            cells[i].classList.add("valid");
            cells[i].classList.remove("invalid");
          } else if(!data["cellsStatus"][i] && data["listOfEditable"][i] && cells[i].innerHTML.trim() !== "0") {
            cells[i].classList.add("invalid");
            cells[i].classList.remove("valid");
          }
          else if(cells[i].innerHTML.trim() === "0"){
            cells[i].classList.remove("valid");
            cells[i].classList.remove("invalid");
          }
        }
        return;
      }
      // else if(!data["editable"] && !data["solved"]){
      //   cells[i].innerHTML = data["val"];
      //   return;
      // }
      else if ( data["solved"]){
        try{
          console.log(data["val"])
          console.log(cells[i].innerHTML.trim());
          cells[i].innerHTML = data["val"] ;
          cells[i].classList.add("valid");
          cells[i].classList.remove("invalid");
        }
        finally{}
        console.log("Ämazingle solved");
        fetch("http://127.0.0.1:5000/complete")
        gameover = true
      }
      
    });
};

// Update cell with the value of the key being pressed if cell is editable
const updateCell = async (val) => {

  for (let i = 0; i < cells.length; i++) {
    cells[i].classList.remove("secondary-focus");
    if (
      cells[i].innerHTML.trim() === val &&
      cells[i].innerHTML.trim() !== "0"
    ) {
      cells[i].classList.add("secondary-focus");
    }
  }

  let i = 0;
  while (i < cells.length) {
    if (cells[i].classList.contains("focus")) {
      pos = cells[i].id.split(" ");
      row_index = +pos[0];
      col_index = +pos[1];
      break;
    }
    i++;
  }
  update(val, row_index, col_index, i);
};

// Manage Timer

var sec = 0;
function pad(val) {
  return val > 9 ? val : "0" + val;
}

// startTimer()
var timeout;
const startTimer = () => {
  document.getElementById("start").innerHTML = ":";
  timeout = setInterval(function () {
    document.getElementById("seconds").innerHTML = pad(++sec % 60);
    document.getElementById("minutes").innerHTML = pad(parseInt(sec / 60, 10));
  }, 1000);
};
// Stop timer

const stopTimer = () => {
  clearInterval(timeout);
};

// Animation

// Fatch animation list from backend(app.py)
// Animation is a list of tuples that contains each value and cell the computer will fill
// Before solving the entire game
const getAnimation = async () => {
  response = await fetch("http://127.0.0.1:5000/solve");
  animation = await response.json();
  return animation;
};

const solve = async (e) => {
  e.preventDefault();
  const animation = await getAnimation();
  if (animation == false) {
    gameover = true;
    return;
  }
  startTimer();
  for (let i = 0; i < animation.length; i++) {
    val = animation[i][0];
    row = animation[i][1];
    col = animation[i][2];
    pos = row * 9 + col;
    setTimeout(await update(val, row, col, pos, addFocusOnAnimation), i * 5);
  }
  stopTimer();
};

document.querySelector("#solve").addEventListener("click", solve);


