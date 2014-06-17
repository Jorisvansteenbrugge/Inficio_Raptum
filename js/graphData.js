function createNodes() {//Functie voor het aanmaken van de nodes
		if(searchCheck==""){
			 nodefile = "Python/nodes.3j";
			 edgefile = "Python/edges.3j";
		}else{
			nodefile = "Python/nodesSearch.3j";
			edgefile = "Python/edgesSearch.3j";
		}
			var pathOfFileToRead = nodefile;//bestand in .3j opmaak
			var contentsOfFileAsString = FileHelper.readStringFromFileAtPath(pathOfFileToRead);//call aan de filehelper function voor het uilezen van .3j
			var mainlist= contentsOfFileAsString.split(":");
			var compoundlist = mainlist[0].split(">");
			compoundlist.shift();
			for (var i = 1; i <= compoundlist.length; i += 1) {
				counter+=1;
				var ids = i//id voor de nodes is gelijk aan het aantal waardes in de array
				var labels = mainlist[0].split("*")[i].split("#")[0];//labels voor de nodes worden uit het bestand gehaald
				var values = mainlist[0].split("#")[i].split("@")[0];// waardes/aantal voorkomens voor nodes worden uit het bestand gehaald
				var title = mainlist[0].split("@")[i].split("+")[0];// titel voor de nodes worden uit het bestand gehald
				nodes.push({// functie die de  voorgaande variabelen in een dictionary voegt en deze toevoegd aan de nodes arraylist met de .push methode
					id: ids,
					value: parseInt(values),
					label: labels,
					title: title,
					shape: 'dot',
					color: "#d52349"
				});
			}
			var organismlist = mainlist[1].split(">");
			organismlist.shift();
			for (var i = 1; i <= organismlist.length; i += 1) {
				var ids = counter+i//id voor de nodes is gelijk aan het aantal waardes in de array
				var labels = mainlist[1].split("*")[i].split("#")[0];//labels voor de nodes worden uit het bestand gehaald;
				var values = mainlist[1].split("#")[i].split("@")[0];// waardes/aantal voorkomens voor nodes worden uit het bestand gehaald
				var title = mainlist[1].split("@")[i].split("+")[0];// titel voor de nodes worden uit het bestand gehald
				nodes.push({// functie die de  voorgaande variabelen in een dictionary voegt en deze toevoegd aan de nodes arraylist met de .push methode
					id: ids,
					value: parseInt(values),
					label: labels,
					title: title,
					shape: 'triangle',
					color: "#eb9f3b"
				});
			}
			createEdges();

		}