var ctx = document.getElementById('myChart').getContext('2d');
var config = {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {},

    // Configuration options go here
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Commodity Price vs Prediction'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'index (30 min intervals)'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }

    }
}


window.myLine = new Chart(ctx, config);
const WINDOW = 20;
let data = []

var randomScalingFactor = function() {
    return Math.random() * 10;
}

var addValDataset = function(datasetName, color) {
    var newDataset = {
        label: datasetName,
        borderColor: color,
        data: [],
        fill: false
    };

    for (var index = 0; index < config.data.labels.length; ++index) {
        newDataset.data.push(randomScalingFactor());
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
}

var addDataset = function() {
    var newDataset = {
        label: 'Dataset ' + config.data.datasets.length,
        data: [],
        fill: false
    };

    for (var index = 0; index < config.data.labels.length; ++index) {
        newDataset.data.push(randomScalingFactor());
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
};

let index = 0
var addValData = function(price, pred) {

    if (config.data.datasets.length > 0) {
        var month = config.data.labels.length;
        config.data.labels.push(index);
        index += 1

        if (pred) {
            config.data.datasets[1].data.push(price)
        } else {
            config.data.datasets[0].data.push(price)

        }
        window.myLine.update();
    }

}

var addData = function() {
    if (config.data.datasets.length > 0) {
        if (config.data.labels.length >= WINDOW) {
            config.data.labels.shift()
            config.data.datasets.forEach(function(dataset) {
                dataset.data.shift()
            })

        }
        var month = config.data.labels.length;
        config.data.labels.push(month);

        config.data.datasets.forEach(function(dataset) {
            dataset.data.push(randomScalingFactor());
        });

        window.myLine.update();
    }
};

addValDataset("Ground Truth", 'rgb(54,162,235)')
addValDataset("Predictions", 'rgb(255,99,132)')

let prev = 0;

$("#spinner").hide()
$("#text").show()

let acc = 0;
let accLength = 0;

var upload_val_price = function() {
    upload_price($("#price_input").val())

}


addValData(0, true)
var upload_price = function(price) {
    var e = document.getElementById("model-selection");
    var strUser = e.options[e.selectedIndex].value;
    $("#text").hide()
    $("#spinner").show()

    let prce = price
    if (prce === "")
        prce = "0"


    accLength += 1;

    $("#price_input").val("")
    data.push(prce);
    addValData(prce, false)

    if (data.length > 9 && config.data.datasets[1].data.length - config.data.datasets[0].data.length === 0) {
        let tempData = data
        let slicedData = tempData.slice(Math.max(data.length - 10, 0))
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: "application/x-www-form-urlencoded",
            data: {
                'slice': slicedData,
                "model": $("#model-selection").val(),
                "timeframe": $("#predict_mode").val()
            },
            dataType: 'json',
            success: function(data) {
                for(var i = 0; i < data.length; i++)
                    addValData(parseFloat(data[i]),true)

                $("#spinner").hide()
                $("#text").show()
            },
            error: function(request, error) {
                alert("Request: " + JSON.stringify(request));
            }
        });
    } else {
        if(data.length <= 9)
            addValData(prev,true)
        $("#spinner").hide()
        $("#text").show()
    }

    prev = prce

    if (accLength > 9) {
        console.log(accLength)
        if (accLength === 11 || accLength === 12 || accLength === 13 || accLength === 14 || accLength === 15 || accLength === 16) {
            config.data.datasets[1].data.shift()
            config.data.datasets[0].data.shift()
            config.data.labels.shift()
        }
        $("#lastprice").html(prce)
        let pred_price = config.data.datasets[1].data[config.data.datasets[1].data.length - 1]
        let percDiff = (Math.abs(prce - pred_price) / prce) * 100
        $("#predprice").html(pred_price)
        acc += percDiff

        $("#curracc").html(acc / (accLength - 10))
        $("#daysrun").html(accLength)

    }

}

let add_init_data = function() {
    let arr = [28.3, 29.33, 29.18, 28.08, 28.08, 28.04, 28.11, 28.06, 28.02, 28.05] // answer should be 28.11
    for (var i = 0; i < arr.length; i++)
        upload_price(arr[i]);
}

$("#test_init_add_data").click(add_init_data)
$("#add_data").click(upload_val_price)
$("#price_input").keypress(function(e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
        upload_val_price()
    }
});

