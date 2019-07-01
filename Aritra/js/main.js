/*
*    main.js
*    Mastering Data Visualization with D3.js
*    2.8 - Activity: Your first visualization!
*/

var margin = { left:80, right:20, top:50, bottom:100 };
var height = 500 - margin.top - margin.bottom, 
    width = 800 - margin.left - margin.right;

var g = d3.select("#chart-area")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + 
            ", " + margin.top + ")");

/*
// Tooltip
var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "<strong>Make:</strong> <span style='color:red'>" + d.make + "</span><br>";
        text += "<strong>Model:</strong> <span style='color:red;text-transform:capitalize'>" + d.model + "</span><br>";
        text += "<strong>Year:</strong> <span style='color:red'>" + d3.format(".2f")(d.year) + "</span><br>";
        text += "<strong>Color:</strong> <span style='color:red'>" + d3.format("$,.0f")(d.color) + "</span><br>";
        return text;
    });
g.call(tip);
*/

// Scales
var x = d3.scaleLog()
    .base(10)
    .range([0, width])
    .domain(["Cadillac"]);
var y = d3.scaleLinear()
    .range([height, 0])
    .domain([0, 90]);
var area = d3.scaleLinear()
    .range([25*Math.PI, 1500*Math.PI])
    .domain([2000, 1400000000]);
var ridetypeColor = d3.scaleOrdinal(d3.schemePastel1);


// Labels
var xLabel = g.append("text")
    .attr("y", height + 50)
    .attr("x", width / 2)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Make of Car");
var yLabel = g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -170)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Number of Rides");

// X Axis
var xAxisCall = d3.axisBottom(x)
    .tickValues([400, 4000, 40000])
    .tickFormat(d3.format("$"));

g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height +")")
    .call(xAxisCall);

// Y Axis
var yAxisCall = d3.axisLeft(y)
    .tickFormat(function(d){ return +d; });
g.append("g")
    .attr("class", "y axis")
    .call(yAxisCall);


var typeOfRides = ["Regular", "Premium", "SUV"];

var legend = g.append("g")
    .attr("transform", "translate(" + (width - 10) + 
        "," + (height - 125) + ")");

typeOfRides.forEach(function(typeOfRide, i){
    var legendRow = legend.append("g")
        .attr("transform", "translate(0, " + (i * 20) + ")");

    legendRow.append("rect")
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", ridetypeColor(typeOfRide));

    legendRow.append("text")
        .attr("x", -10)
        .attr("y", 10)
        .attr("text-anchor", "end")
        .style("text-transform", "capitalize")
        .text(typeOfRide);
});
            
d3.csv("data/austin_rideshare_2.csv").then(function(data){
    console.log(data);


    // Clean data
    formattedData = data.map(function(year){
        return year["rides"].filter(function(requested_car_category){
            var dataExists = (requested_car_category.make && requested_car_category.date);
            return dataExists
        })
    });    
$("#play-button")
.on("click", function(){
    var button = $(this);
    if (button.text() == "Play"){
        button.text("Pause");
        interval = setInterval(step, 100);            
    }
    else {
        button.text("Play");
        clearInterval(interval);
    }
})

$("#reset-button")
.on("click", function(){
    time = 0;
    update(formattedData[0]);
})

// First run of the visualization
    update(formattedData[0]);
});

// JOIN new data with old elements.
var circles = g.selectAll("circle").data(data, function(d){
    return d.requested_car_category;
});

// EXIT old elements not present in new data.
circles.exit()
    .attr("class", "exit")
    .remove();