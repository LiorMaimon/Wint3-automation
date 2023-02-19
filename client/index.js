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