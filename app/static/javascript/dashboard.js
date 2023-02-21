$(document).ready(function () {
  window.onload = function () {
    $.ajax({ url: "api/financedata/all/15" }).done(function (res) {
      const keys = Object.keys(res);
      keys.forEach((element) => {
        amount = res[element][0].toFixed(2);
        category = res[element][1];
        description = res[element][2];
        if (amount > 0) {
          $("#history_list").append(
            $(
              "<li class='list-group-item d-flex justify-content-between align-items-start'>"
            ).html(
              '<div style="display: flex;align-items: center; width:100%;"><div class="ms-2" style="flex: 1; text-align: left;"><div class="fw-bold" style="font-size: 2vh;">' +
                String(category) +
                '</div><div style="font-size: 1.5vh;">' +
                String(description) +
                '</div></div><div class="fw-bold" style="font-size: 2vh; color: #00d431; flex: 1; text-align: right;">' +
                String(amount) +
                "€</div></div>"
            )
          );
        } else {
          $("#history_list").append(
            $(
              "<li class='list-group-item d-flex justify-content-between align-items-start'>"
            ).html(
              '<div style="display: flex;align-items: center; width:100%;"><div class="ms-2" style="flex: 1; text-align: left;"><div class="fw-bold" style="font-size: 2vh;">' +
                String(category) +
                '</div><div style="font-size: 1.5vh;">' +
                String(description) +
                '</div></div><div class="fw-bold" style="font-size: 2vh; color: red; flex: 1; text-align: right;">' +
                String(amount) +
                "€</div></div>"
            )
          );
        }
      });
    });
  };
});
