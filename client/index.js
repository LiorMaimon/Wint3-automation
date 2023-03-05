host = windows.location.href;

function MyOnLoad() {
    update_status();
}

function update_status() {
    fetch(host + "results", {
          method: "GET",
        })
        .then((response) => {
            return response.json();
          })
          .then((jresponse) => {
            var html = "";
            for (var key in jresponse) {
                key.replace(/\\/g, '');
                result = document.getElementById(key + "_result");
                html += "<p><b>" + key + ":</b> " + jresponse[key] + "</p>";
            }
            result.innerHTML = html;          })
          .catch((error) => {
            console.error("Error:", error);
          });
    SetTimeout(update_status, 4000);
    }
}


document.addEventListener("DOMContentLoaded", function() {
          setInterval(function() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                var result = document.getElementById("open_valve_result");
                var response = JSON.parse(xhr.responseText);
                var html = "";
                for (var key in response) {
                  key.replace(/\\/g, '');
                  result = document.getElementById(key + "_result");
                  html += "<p><b>" + key + ":</b> " + response[key] + "</p>";
                }
                result.innerHTML = html;
              }
            };
            xhr.open("GET", "/results", true);
            xhr.send();
          }, 4000);
        });

      }


const form = document.getElementById("myForm");
const radioButtons = document.getElementsByName("option");
form.addEventListener("submit", (e) => {
e.preventDefault();
const checkboxes = form.elements;
const selected = [];
const select_radio = null
for (let i = 0; i < checkboxes.length; i++) {
  if (checkboxes[i].type === "checkbox" && checkboxes[i].checked) {
    selected.push(checkboxes[i].name);
    }
  if (radioButtons[i].checked){
    selected_radio = radioButtons[i].value;
    }
}
fetch("/run_command", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    selected: selected,
  }),
})
  .then((response) => {
    return response.text();
  })
  .then((htmlContent) => {
    const responseContent = document.getElementById("response-content");
    responseContent.innerHTML += htmlContent;
  })
  .catch((error) => {
    console.error("Error:", error);
  });
});