$(function() {
    $('input[name="daterange"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            cancelLabel: 'Clear'
        },
        maxDate: new Date()
    },
        function(start, end) {
            change_history(start, end);
        }
    );
  
    $('input[name="daterange"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
    });
  
    $('input[name="daterange"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('Select time range');
        $('#history_list_stats').empty()
    });
});

function get_history_data() {
return new Promise((resolve) => {
    $.ajax({ url: "api/financedata/all/9999999" }).done(function (res) {
        resolve(res);
    });
});
}

async function change_history(start, end) {
    const data = await get_history_data();
    const options = {year: 'numeric', month: 'numeric', day: 'numeric' };
    const keys = Object.keys(data);
    $('#history_list_stats').empty()
    keys.forEach((element) => {
      amount = data[element][0].toFixed(2);
      category = data[element][1];
      description = data[element][2];
      date = data[element][3];
      if (new Date(start).getTime() <= new Date(date*1000) && new Date(end).getTime() >= new Date(date*1000)){
        if (amount > 0) {
            $("#history_list_stats").append(
              $(
                "<li class='list-group-item d-flex justify-content-between align-items-start'>"
              ).html(
                  '<div style="display: flex;align-items: center; width:100%;"><div class="fw" style="font-size: 2vh;">' +
                  String(new Date(date*1000).toLocaleDateString("lv-LV", options)) +
                  '</div><div class="ms-2" style="flex: 1; text-align: left;"><div class="fw-bold" style="font-size: 2vh;">' +  
                  String(category) +
                  '</div><div style="font-size: 1.5vh;">' +
                  String(description) +
                  '</div></div><div class="fw-bold" style="font-size: 2vh; color: #00d431; flex: 1; text-align: right;">' +
                  String(amount) +
                  "€</div></div>"
              )
            );
          } else {
            $("#history_list_stats").append(
              $(
                "<li class='list-group-item d-flex justify-content-between align-items-start'>"
              ).html(
                '<div style="display: flex;align-items: center; width:100%;"><div class="fw" style="font-size: 2vh;">' +
                  String(new Date(date*1000).toLocaleDateString("lv-LV", options)) +
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
      };
    });
  };

