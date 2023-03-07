// Ielādē Google Charts grafiku veidošanas api
google.charts.load("current", { packages: ["corechart"] });

// Pievieno callback funkciju, kas nostrādā uzreiz kad ir ielādējies api, lai izveidotu grafikus
google.charts.setOnLoadCallback(draw_line_chart);

// Nosūta pieprasījumu serverim, kas atgriež nepieciešamos datus grafiku izveidei
function get_graph_data(timeframe, timeframe_amount) {
  return new Promise((resolve) => {
    $.ajax({ url: "api/graphdata/" + timeframe + "/" + timeframe_amount }).done(function (res) {
      resolve(res);
    });
  });
}

// Funkcija, kas apstrādā iegūtos datus, lai parādītu tos grafikā
async function draw_line_chart() {
  var timeframe, timeframe_amount;
  // Iegūst izvēlēto laika perioda pogas vērtību
  radio_data = document.querySelector('input[name="timeframe_selector"]:checked').id.split("_");
  timeframe = radio_data[0]
  timeframe_amount = radio_data[1]
  // Iegūst kādu grafiu parādīt - income vai expense
  type = document.querySelector('input[name="type_selector"]:checked').id.split("_")[0].toLowerCase();
  // Pieprasa datus no servera
  const graph_data = await get_graph_data(timeframe, timeframe_amount);

  // Ievieto iegūtos datus Google data table
  var income_data = new google.visualization.DataTable();
  income_data.addColumn("datetime", "Date")
  income_data.addColumn("number", "Amount")

  graph_data["income"].forEach((row) => {
    income_data.addRow([new Date(row[1]*1000), row[0]]);
  });

  var expense_data = new google.visualization.DataTable();
  expense_data.addColumn("datetime", "Date")
  expense_data.addColumn("number", "Amount")

  graph_data["expense"].forEach((row) => {
    expense_data.addRow([new Date(row[1]*1000), -row[0]]);
  });

  // Iestata grafiku izskata iestatījumus
  var options = {
    chartArea: {"width": "85%", "height": "75%"},
    vAxis: {format: '\u20AC#.##'},
    hAxis: {gridlines:{count:5}, format:"dd.MM.Y"},
    legend: "none",
    pointSize: 8,
  };

  // Izvēlas attiecīgo html elementu un pievieno tam attiecīgi izveidoto grafiku
  // Bilances grafiks
  var chart = new google.visualization.LineChart(
    document.getElementById("balance_history_graph")
  );
  chart.draw(income_data, options);
  
  // Ienākumu/izdevumu grafiks
  var chart = new google.visualization.LineChart(
    document.getElementById("income_expense_history_graph")
  );
  if (type == "income"){
    chart.draw(income_data, options);
  }
  else {
    chart.draw(expense_data, options); 
  }
}

// Funkcija, ko izmanto pogas, lai atjaunotu grafikus, mainot laika vai tipa izvēles
function update_line_charts() {
  draw_line_chart()
}