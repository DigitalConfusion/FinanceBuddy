// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    // Set Data
    var data = google.visualization.arrayToDataTable([
      ['Price', 'Size'],
      [50,7],[60,8],[70,8],[80,9],[90,9],[100,9],
      [110,10],[120,11],[130,14],[140,14],[150,15]
      ]);
    // Set Options
    var options = {
        "chartArea": {"width": "90%", "height": "80%"},
        "legend": "none"
    };
    // Draw Chart
    var chart = new google.visualization.LineChart(document.getElementById('balance_history_graph'));
    chart.draw(data, options);
    var chart = new google.visualization.LineChart(document.getElementById('balance_history_graph2'));
    chart.draw(data, options);
    }