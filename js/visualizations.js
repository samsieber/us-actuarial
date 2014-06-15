var Visualizer = (function Visualizer_namespace(){
	function Visualizer(tagname){
		console.log("HERE", tagname)
		var margin = {top: 20, right: 20, bottom: 30, left: 40},
			width = 1000 - margin.left - margin.right,
			height = 500 - margin.top - margin.bottom;

		var svg = d3.select("body").append("svg")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
		  .append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
			
		var x = d3.scale.ordinal()
			.rangeRoundBands([0, width], .1);

		var y = d3.scale.linear()
			.range([height, 0]);

		var xAxis = d3.svg.axis()
			.scale(x)
			.orient("bottom")
			.tickValues([1900,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010]);

		var yAxis = d3.svg.axis()
			.scale(y)
			.orient("left")
			.ticks(10);
			
		console.log("HERE1")
		this.useDataSource = function(dataSource){
			
			console.log("HERE - Coming forth with data", dataSource)
			var data = dataSource.datapoints;
			var title = dataSource.getTitle();
			
			x.domain(data.map(function(d) { return d.year; }));
			y.domain([0, d3.max(data, function(d) { return d.born; })]);

			svg.append("g")
			  .attr("class", "x axis")
			  .attr("transform", "translate(0," + height + ")")
			  .call(xAxis);

			svg.append("g")
			  .attr("class", "y axis")
			  .call(yAxis)
			.append("text")
			  .attr("transform", "rotate(-90)")
			  .attr("y", 6)
			  .attr("dy", ".71em")
			  .style("text-anchor", "end")
			  .text("Frequency");
			
			addBar("born",function(d) { return y(d.born); })
			addBar("alive",function(d) { return y(d.born * d.percent); })
			
			function addBar(class_tag,y_getter){
				svg.selectAll("." + class_tag)
				  .data(data)
				.enter().append("rect")
				  .attr("class", class_tag)
				  .attr("x", function(d) { return x(d.year); })
				  .attr("width", x.rangeBand())
				  .attr("y", y_getter)
				  .attr("height", function(d) { return height - y_getter(d) });
			}
			
			function type(d) {
			  d.frequency = +d.frequency;
			  return d;
			}
		};			
	}
	
	var proto = Visualizer.prototype;
	
	console.log("SDFSDFSDF");
	return Visualizer;
}());

console.log("ASD");
