var gameover = false;

cells = document.querySelectorAll("div.cell");
subcells = document.querySelectorAll("div.sub-cell");


// Check if all the cells in the board are empty and return true if they are all empty

const cellAllEmpty = () => {
  let allempty = true;
  for (let i = 1; i < cells.length; i++) {
    if (cells[i].innerHTML.trim().length != 0) {
      allempty = false;
    }
  }
  return allempty;
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

// Listening to key press
addEvent(document, "keydown", function (e) {
  e = e || window.event;
  const key =
    e.key !== "Backspace" && e.key !== "0"
      ? e.key
      : e.key == "Backspace"
      ? "0"
      : null;
  if (
    ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"].includes(key) &&
    !gameover
  ) {
    updateCell(key);
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

cells.forEach((cell) => {
  cell.addEventListener("click", addFocus);
});

subcells.forEach((cell) => {
  cell.addEventListener("click", () => updateCell(cell.innerHTML.trim()));
});

//  Update the grid in the backend and the frontend with the new information of a particular cell
const update = async (val, row_index, col_index, i = 0, fnc = () => {}) => {
  fnc(val, i);
  if (gameover) {
    return null;
  }
  const response = await fetch(window.location.href, {
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
      if (data.editable && !data.solved) {
        cells[i].innerHTML = +data.val !== 0 ? data.val : null;
        // Updating the background color of each cell based on the validity of their value
        for (let i = 0; i < data.cellsStatus.length; i++) {
          if (
            data.cellsStatus[i] &&
            data.listOfEditable[i] &&
            cells[i].innerHTML.trim() !== null
          ) {
            cells[i].classList.add("valid");
            cells[i].classList.remove("invalid");
          } else if (
            !data.cellsStatus[i] &&
            data.listOfEditable[i] &&
            cells[i].innerHTML.trim() !== null
          ) {
            cells[i].classList.add("invalid");
            cells[i].classList.remove("valid");
          }
        }
        // remove styling on all the empty cells
        for (let i = 0; i < cells.length; i++) {
          if (cells[i].innerHTML.trim().length === 0) {
            cells[i].classList.remove("valid");
            cells[i].classList.remove("invalid");
          }
        }
        return;
      } else if (data.solved) {
        try {
          cells[i].innerHTML = data.val;
          cells[i].classList.add("valid");
          cells[i].classList.remove("invalid");
        } finally {
          stopTimer();
          document.getElementById("complete").style.display = "flex";
        }
        // Updating the background color of each cell based on the validity of their value
        for (let i = 0; i < data.cellsStatus.length; i++) {
          if (
            data.cellsStatus[i] &&
            data.listOfEditable[i] &&
            cells[i].innerHTML.trim() !== null
          ) {
            cells[i].classList.add("valid");
            cells[i].classList.remove("invalid");
          } else if (
            !data.cellsStatus[i] &&
            data.listOfEditable[i] &&
            cells[i].innerHTML.trim() !== null
          ) {
            cells[i].classList.add("invalid");
            cells[i].classList.remove("valid");
          }
        }
        stopTimer();
        gameover = true;
        return;
      }
    });
};

// Update cell with the value of the key being pressed if cell is editable
const updateCell = async (val) => {
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
  if (i === 81) {
    return; //  stop the function if no cell is focused
  }

  for (let i = 0; i < cells.length; i++) {
    cells[i].classList.remove("secondary-focus");
    if (
      cells[i].innerHTML.trim() === val &&
      cells[i].innerHTML.trim() !== "0"
    ) {
      cells[i].classList.add("secondary-focus");
    }
  }

  update(val, row_index, col_index, i);
};

// Animation

// Fatch animation list from backend(app.py)
// Animation is a list of tuples that contains each value and cell the computer will fill
// Before solving the entire game
const getAnimation = async () => {
  response = await fetch('/solve');
  animation = await response.json();
  return animation;
};

const solve = async (e) => {
  e.preventDefault();
  //  check if all the cells are empty, then there is nothing to solve
  let allempty = true;
  if (cellAllEmpty()) {
    return;
  }

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
};

document.querySelector("#solve").addEventListener("click", solve);

// Difficulty Level

const setLevel = async (e) => {
  url_ = window.location.href.indexOf('play') < 0 ? '/play/' : window.location.href
  response = await fetch(url_, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      level: e.target.value,
    }),
  }).then((res) => res.json())
    .then(data => {
        window.location.href = `/play/${data.level}`
        e.target.value = data.level;
    })
};

document.getElementById("level").addEventListener("change", setLevel);


const newGame = () => {
  if (window.location.href.indexOf('play') >= 0){
    window.location.reload()
  }
  else{
    window.location.href = '/play/'
  }
        
}
