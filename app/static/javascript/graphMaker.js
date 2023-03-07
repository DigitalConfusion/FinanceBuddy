// Load the Visualization API and the corechart package.
google.charts.load("current", { packages: ["corechart"] });

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(draw_line_chart);

function get_graph_data(timeframe, timeframe_amount) {
  return new Promise((resolve) => {
    $.ajax({ url: "api/graphdata/" + timeframe + "/" + timeframe_amount }).done(function (res) {
      resolve(res);
    });
  });
}

async function draw_line_chart() {
  var timeframe, timeframe_amount;
  radio_data = document.querySelector('input[name="timeframe_selector"]:checked').id.split("_");
  timeframe = radio_data[0]
  timeframe_amount = radio_data[1]
  type = document.querySelector('input[name="type_selector"]:checked').id.split("_")[0].toLowerCase();
  const graph_data = await get_graph_data(timeframe, timeframe_amount);

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

  // Set Options
  var options = {
    chartArea: {"width": "85%", "height": "75%"},
    vAxis: {format: '\u20AC#.##'},
    hAxis: {gridlines:{count:5}, format:"dd.MM.Y"},
    legend: "none",
    pointSize: 8,
  };

  // Draw Charts
  var chart = new google.visualization.LineChart(
    document.getElementById("balance_history_graph")
  );
  chart.draw(income_data, options);

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

function update_line_charts() {
  draw_line_chart()
}