function drawGraph() {
	// Instantiate our graph object.
	var container = document.getElementById('mygraph');
	var data = {
		nodes: nodes,
		edges: edges
	};

	var options = {
		width: '1000px',
		height: '500px',
		edges: {
			color: '#97C2FC'
		},
		dataManipulation: true,
		//clustering: true,
		initiallyVisible: true


	};


	graph = new vis.Graph(container, data, options);
	graph.on('doubleClick', function (properties) { //Double click event on nodes
		document.getElementById("tabbeldiv").innerHTML = '\
			   <table id="itemList">\
			   		<thead>\
			   			<tr>\
			   				<td><b>Title</b></td>\
			   				<td><b>Pubmed_ID</b></td>\
			   				<td><b>Abstract</b></td>\
			   			</tr>\
			   		</thead>\
			   		<tbody>\
					</tbody>\
			   </table>';
		var id = properties.nodes;
		var selected = nodes[id - 1]["title"].split(",");
		selected.pop();
		var rows = "";
		var items = [];



		for (var i = 0; i <= titles.length; i += 1) {
			if (pubids[i] == undefined) {
				//doe niks
			} else {
				var pubid = pubids[i].replace(" ", "");
				if (selected.indexOf(pubid) >= 0) {
					var tit = titles[i];
					var abst = abstracts[i];
					items.push({
						Title: tit,
						Pubmed_ID: pubid,
						Abstract: abst
					});
				} else {}
			}
		}

		$.each(items, function () {
			rows += "<tr><td>" + this.Title + "</td><td>" + this.Pubmed_ID + "</td><td>" + this.Abstract + "</td></tr>";
		});

		$(rows).appendTo("#itemList tbody");
	});

}
// JavaScript Document