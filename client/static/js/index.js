
function paintClick(){

      $('input[type="checkbox"]').click(function() {
        if($(this).is(':checked')) {
          $(this).closest('tr').css('background-color', '#DAF8FC');
        } else {
          $(this).closest('tr').css('background-color', '');
        }
      });
}

function runCommandRequest(){
    const form = document.getElementById("myForm");
    const radioButtons = document.getElementsByName("option");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const checkboxes = form.elements;
      const selected = [];
      let selectedRadio = null
      for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].type === "checkbox" && checkboxes[i].checked) {
          selected.push(checkboxes[i].name);
          }
      }
      for (let i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
          selectedRadio = radioButtons[i].value;
          break;
        }
      }
      fetch("/run_command", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          selected: selected,
          selected_radio: selectedRadio,
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
}

function updateResultCol(){
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
              html += "<p><b>"  + "</b> " + response[key] + "</p>";
            }
            if (html !== ("")){
              result.innerHTML = html;
            }
          }
        };
        xhr.open("GET", "/results", true);
        xhr.send();
      }, 4000);
    });
}