// Kad dokuments ir ielādējies un gatavs reģidēšanai
$(document).ready(function () {
  // Funkcija kas nostrādā uz lapas ielādēšanos un izveido ienākumu/izdevumu vēsturi
  window.onload = function () {
    // Nosūta pieprasījumu uz serveri, lai kopā iegūtu pēdējos 15 ienākumus/izdevumus
    $.ajax({ url: "api/financedata/all/15" }).done(function (res) {
      const keys = Object.keys(res);
      // Iet cauri katram atgrieztajam ierakstam
      keys.forEach((element) => {
        // Ievieto nepieciešamo informāciju mainīgajos
        amount = res[element][0].toFixed(2);
        category = res[element][1];
        description = res[element][2];
        // Ja dotais ieraksts ir ienākums, tad pievieno to vēsturei ar plus zīmi un zaļu naudas summu
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
        }
        // Ja dotais ieraksts ir izdevums, tad pievieno to vēsturei ar mīnuss zīmi un sarkanu naudas summu
        else {
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
  // Pašā sākumā paslēpj custom category ierakstīšas iespējas ienākumu/izdevumu pievienošanas logā
  document.getElementById("custom_category").style.display = "none";
  document.getElementById("custom_category2").style.display = "none";
});

// Funkcija, kas pievieno kategorijas izvēles mainīgajam onclick eventu, kas pārbauda
// vai nav izvēlēta custom category, ja ir tad parāda custom category ievadīšanas logu
(() => {
  const selectElem = document.getElementById("income_category");
  selectElem.addEventListener("change", (evt) => {
    if (selectElem.value == "Custom Category") {
      document.getElementById("custom_category").style.display = "flex";
    } else {
      document.getElementById("custom_category").style.display = "none";
    }
  });
})();

// Funkcija, kas pievieno kategorijas izvēles mainīgajam onclick eventu, kas pārbauda
// vai nav izvēlēta custom category, ja ir tad parāda custom category ievadīšanas logu
(() => {
  const selectElem = document.getElementById("expense_category");
  selectElem.addEventListener("change", (evt) => {
    if (selectElem.value == "Custom Category") {
      document.getElementById("custom_category2").style.display = "flex";
    } else {
      document.getElementById("custom_category2").style.display = "none";
    }
  });
})();
