function NameProxy(gender){
	this.gender = gender[0].toUpperCase();
}

NameProxy.prototype.init = function(){
	var self = this;
	return Promise.all([Promise.resolve($.getJSON( "files/"+self.gender + "/index.json")).then(function(data){
		self.first_year = data.first_year;
		self.partitions = data.first_names.map(function(name){return name.toLowerCase()});
		self.names = data.all_names.map(function(name){return name.toLowerCase()})
		self.is_valid = [];
		self.index = [];
		self.names.forEach(function add_is_valid(name){
			self.is_valid[name] = true;
		});
		return true;
	}),
	Promise.resolve($.getJSON("files/"+self.gender + "/dist.json")).then(function(data){
		self.dist = data;
	})])
}

NameProxy.prototype.fetchName = function(name){
	var proxy = this;
	name = name.toLowerCase();
	if (!proxy.is_valid[name])
		throw Error("This is not a valid name")
	if (!proxy.index[name])
		console.log("Fetching name file!")
	else 
		return new Promise(function(resolve, reject){resolve(proxy.index[name])})
		
	var name_file_name = proxy.getIndexFileName(name).toLowerCase();
	return Promise.resolve($.get( "files/"+proxy.gender + "/"+name_file_name+".csv")).then(function(data){
		proxy.useDataFromCSV(data);
		console.log("Alive");
		return proxy.index[name];
	})
}

NameProxy.prototype.useDataFromCSV = function (csv){
	var arr = CSVToArray(csv);
	var proxy = this;
	arr.forEach(function index_name(name_row){
		proxy.index[name_row.shift()] = name_row;
	});
}

NameProxy.prototype.getIndexFileName = function (name){
	console.log(name);
	for (var i = this.partitions.length - 1; i >=0 ; i--) {
		if (name >= this.partitions[i]) return this.partitions[i]
	}
	return this.partitions[this.partitions.length-1];
}
