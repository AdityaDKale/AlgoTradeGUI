function timeToIST(originalTime) {
    const timeZone = 'Asia/Kolkata';
    const utcOffset = 5.5 * 60 * 60; // 5.5 hours offset for IST
    const zonedTime = originalTime + utcOffset;
    return zonedTime;
}

function buyCall() {
    fetch('/buyCall')
        .then(response => response.json())
        .then(data => {
            const message = data.order.message; // Extract the message from the order object
            showToastMessage(message);
        });
}

function sellCall() {
    fetch('/sellCall')
        .then(response => response.json())
        .then(data => {
            const message = data.order.message; // Extract the message from the order object
            showToastMessage(message);
        });
}

function buyPut() {
    fetch('/buyPut')
        .then(response => response.json())
        .then(data => {
            const message = data.order.message; // Extract the message from the order object
            showToastMessage(message);
        });
}

function sellPut() {
    fetch('/sellPut')
        .then(response => response.json())
        .then(data => {
            const message = data.order.message; // Extract the message from the order object
            showToastMessage(message);
        });
}


function showToastMessage(message) {
    const toastMessageElement = document.getElementById('toastMessage');
    toastMessageElement.innerText = message;
    const liveToast = new bootstrap.Toast(document.getElementById('liveToast'), { delay: 30000 });
    liveToast.show();
}



document.addEventListener('DOMContentLoaded', function () {
    var selectedSymbol = document.getElementById("data-container").dataset.symbol;
    var selectedTimeFrame = document.getElementById("data-container").dataset.timeFrame;

    function fetchData(symbol = selectedSymbol, timeFrame = selectedTimeFrame) {
        fetch(`/data?symbol=${symbol}&time_frame=${timeFrame}`)
            .then(response => response.json())
            .then(data => {
                const screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
                const screenHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

                const desiredWidth = Math.floor(screenWidth * 0.7);
                const desiredHeight = Math.floor(screenHeight * 1);

                const chart = LightweightCharts.createChart(document.getElementById('chartContainer'), {
                    width: desiredWidth,
                    height: desiredHeight,
                    localization: {
                        timeFormatter: businessDayOrTimestamp => {
                            const timeStamp = timeToIST(businessDayOrTimestamp / 1000) * 1000;
                            return new Date(timeStamp).toLocaleString();
                        },
                    },
                });

                chart.applyOptions({
                    crosshair: {
                        // Change mode from default 'magnet' to 'normal'.
                        // Allows the crosshair to move freely without snapping to datapoints
                        mode: LightweightCharts.CrosshairMode.Normal,

                        // Vertical crosshair line (showing Date in Label)
                        vertLine: {
                            width: 8,
                            color: '#C3BCDB44',
                            style: LightweightCharts.LineStyle.Solid,
                            labelBackgroundColor: '#9B7DFF',
                        },

                        // Horizontal crosshair line (showing Price in Label)
                        horzLine: {
                            color: '#9B7DFF',
                            labelBackgroundColor: '#9B7DFF',
                        },
                    },
                });

                chart.applyOptions({
                    timeScale: {
                        borderColor: '#71649C',
                        timeVisible: true, // Display the time scale
                        secondsVisible: false, // Do not display seconds
                    },
                });

                const candleSeries = chart.addCandlestickSeries();
                candleSeries.setData(data);

                const legend = document.getElementById('legend');

                const updateLegend = param => {
                    const validCrosshairPoint = !(param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0);
                    const bar = validCrosshairPoint ? param.seriesData.get(candleSeries) : candleSeries.lastValue();
                    const open = bar.open
                    const high = bar.high
                    const low = bar.low
                    const close = bar.close;
                    const legendText = `<table><tr><td>Open</td><td>${open}</td><td>High</td><td>${high}</td><td>Low</td><td>${low}</td><td>Close</td><td>${close}</td></tr></table>`
                    legend.innerHTML = legendText;
                };

                chart.subscribeCrosshairMove(updateLegend);
            })
            .catch(error => console.error(error));
    }

    function updateData(symbol, timeFrame) {
        // Clear existing chart container and legend
        const chartContainer = document.getElementById('chartContainer');
        chartContainer.innerHTML = '';
        document.getElementById('legend').innerHTML = '';

        // Update the stock header with the selected symbol and time frame
        const stockNameElement = document.getElementById('stockName');
        const timeFrameElement = document.getElementById('timeFrame');
        stockNameElement.innerText = symbol;
        timeFrameElement.innerText = timeFrame;

        fetchData(symbol, timeFrame);
    }

    // Initial data fetch
    const symbolRows = document.getElementsByClassName('symbol-row');
    fetchData(selectedSymbol, selectedTimeFrame); // Fetch data for the initial symbol and time frame

    Array.from(symbolRows).forEach(row => {
        row.addEventListener('click', function () {
            selectedSymbol = this.dataset.symbol;
            updateData(selectedSymbol, selectedTimeFrame); // Update the data with the selected symbol and current time frame
        });
    });

    const timeFrameList = document.getElementById('timeFrameList');
    timeFrameList.value = selectedTimeFrame; // Set the initial selected value in the dropdown

    // Update the selected time frame in the dropdown when it changes
    timeFrameList.addEventListener('change', function () {
        selectedTimeFrame = timeFrameList.value;
        updateData(selectedSymbol, selectedTimeFrame);
    });

    // Update the dropdown selection on page load
    // updateDropdown();
    initialize();
});
