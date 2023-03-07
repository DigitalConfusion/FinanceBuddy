// Funkcija, priekš datumu izvēles vēstures datu parādīšanai
$(function () {
  // Pievieno datumu izvēlētāju attiecīgajam html elementam
  $('input[name="daterange"]').daterangepicker(
    {
      // Iestatījumi
      autoUpdateInput: false,
      locale: {
        cancelLabel: "Clear",
      },
      maxDate: new Date(),
    },
    // Funkcija, ko darbina, kad datums izvēlēts
    function (start, end) {
      change_history(start, end);
    }
  );
  // Atjaunina logā parādīto datumu
  $('input[name="daterange"]').on(
    "apply.daterangepicker",
    function (ev, picker) {
      $(this).val(
        picker.startDate.format("DD/MM/YYYY") +
          " - " +
          picker.endDate.format("DD/MM/YYYY")
      );
    }
  );
  // Notīra izvēlēto datumu, ja datums nav izvēlēts
  $('input[name="daterange"]').on(
    "cancel.daterangepicker",
    function (ev, picker) {
      $(this).val("Select time range");
      $("#history_list_stats").empty();
    }
  );
});

// Funkcija, kas nosūta pieprasījumu serverim, vēstures datu izveidošanai
function get_history_data() {
  return new Promise((resolve) => {
    $.ajax({ url: "api/financedata/all/9999999" }).done(function (res) {
      resolve(res);
    });
  });
}

// Funkcija, kas atjaunina vestures datus, pēc cita datuma izvēlēšanās
async function change_history(start, end) {
  // Pieprasa datus no servera
  const data = await get_history_data();
  // Ciparu veida mēnešu formāta opciju izvēle
  const options = { year: "numeric", month: "numeric", day: "numeric" };
  const keys = Object.keys(data);
  // Notīra iepriekšējos vēsture ierakstus elementā
  $("#history_list_stats").empty();
  // Iet cauri katrai iegūto datu rindiņai
  keys.forEach((element) => {
    // Piesaista nepieciešamos datus mainīgajiem
    amount = data[element][0].toFixed(2);
    category = data[element][1];
    description = data[element][2];
    date = data[element][3];
    // Pārbauda vai ieraksts ir starp izvēlēto laika periodu
    if (
      new Date(start).getTime() <= new Date(date * 1000) &&
      new Date(end).getTime() >= new Date(date * 1000)
    ) {
      // Ja dotais ieraksts ir ienākums, tad pievieno to vēsturei ar plus zīmi un zaļu naudas summu
      if (amount > 0) {
        $("#history_list_stats").append(
          $(
            "<li class='list-group-item d-flex justify-content-between align-items-start'>"
          ).html(
            '<div style="display: flex;align-items: center; width:100%;"><div class="fw" style="font-size: 2vh;">' +
              String(
                new Date(date * 1000).toLocaleDateString("lv-LV", options)
              ) +
              '</div><div class="ms-2" style="flex: 1; text-align: left;"><div class="fw-bold" style="font-size: 2vh;">' +
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
        $("#history_list_stats").append(
          $(
            "<li class='list-group-item d-flex justify-content-between align-items-start'>"
          ).html(
            '<div style="display: flex;align-items: center; width:100%;"><div class="fw" style="font-size: 2vh;">' +
              String(
                new Date(date * 1000).toLocaleDateString("lv-LV", options)
              ) +
              '</div><div class="ms-2" style="flex: 1; text-align: left;"><div class="fw-bold" style="font-size: 2vh;">' +
              String(category) +
              '</div><div style="font-size: 1.5vh;">' +
              String(description) +
              '</div></div><div class="fw-bold" style="font-size: 2vh; color:red; flex: 1; text-align: right;">' +
              String(amount) +
              "€</div></div>"
          )
        );
      }
    }
  });
}
