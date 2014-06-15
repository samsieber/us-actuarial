"use strict";

var NameData = (function NameDataCalculator_namespace(){
	function NameData(request, datapoints){
		this.request = request
		this.datapoints = datapoints
	}
	
	var proto = NameData.prototype;
	
	proto.getTitle = function(){
		return this.request.name + " (" + this.request.gender + ")";
	};
	
	return NameData;
}());

var NameAgeFetcher = (function NameAgeFormatter_namespace(){
	
	function NameAgeFetcher(){
		this.women = new NameProxy("F")
		this.men = new NameProxy("M")
	}
	
	var proto = NameAgeFetcher.prototype;
	
	proto.init = function(){
		return Promise.all([this.women.init(),this.men.init()])	
	};
	
	proto.getProxy = function(request){
		if (request.gender == "Female") return this.women
		if (request.gender == "Male") return this.men
		return this.men
	}
	
	proto.getData = function(request){
		var self = this;
		var proxy = this.getProxy(request);
		return proxy.fetchName(request.name).then(function(name_data){
			console.log(name_data)
			console.log(proxy.dist)
			var retval = new NameData(
				request,
				name_data.map(function(value, index){
					var year = parseInt(index+proxy.first_year),
						born = parseInt(value),
						percent = parseFloat(proxy.dist[year] || 0)
					return {born:born, percent:percent, year:year }
				})
			);
			console.log(retval)
			return retval
		});
		
	};
	
	return NameAgeFetcher;
}());
