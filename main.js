    var width = 1600,
        height = 1200;

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .gravity(.1)
        .distance(500)
        .charge(-30)
        .size([width, height]);

    d3.json("data.json", function(json) {
      force
          .nodes(json.nodes)
          .links(json.links)
          .start();

      var link = svg.selectAll(".link")
          .data(json.links)
        .enter().append("line")
          .attr("class", "link")
        .style("stroke-width", function(d) { return Math.sqrt(d.weight); });

      var node = svg.selectAll(".node")
          .data(json.nodes)
        .enter().append("g")
          .style("fill", function (d) {
          	return "blue"; 
          })
          .attr("class", "node")
          .call(force.drag)
          .on('dblclick', connectedNodes);

      node.append("circle")
          .attr("r","5");

      node.append("text")
          .attr("dx", 12)
          .attr("dy", ".35em")
          .text(function(d) { return d.name });

      force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
      });

      var toggle = 0; 
	  var linkedByIndex = {};
	  for (i = 0; i < json.nodes.length; i++) {
	      linkedByIndex[i + "," + i] = 1;
	  };
	  json.links.forEach(function (d) {
	      linkedByIndex[d.source.index + "," + d.target.index] = 1;
	  });
	  function neighboring(a, b) {
	      return linkedByIndex[a.index + "," + b.index];
	  }
	  function connectedNodes() {
	      if (toggle == 0) {
	          d = d3.select(this).node().__data__;
	          node.style("opacity", function (o) {
	              return neighboring(d, o) | neighboring(o, d) ? 1 : 0.1;
	          });
	          link.style("opacity", function (o) {
	              return d.index==o.source.index | d.index==o.target.index ? 1 : 0.1;
	          });
	          toggle = 1;
	      } else {
	          node.style("opacity", 1);
	          link.style("opacity", 1);
	          toggle = 0;
	      }
	  }

	  var optArray = [];
	  for (var i = 0; i < json.nodes.length - 1; i++) {
    	optArray.push(json.nodes[i].name);
  	  }

  	  optArray = optArray.sort();

	  $(function () {
	    $("#search").autocomplete({
	        source: optArray
	      });
	  });


    });

 function searchNode() {

	var selectedVal = document.getElementById('search').value;
	var node = svg.selectAll(".node");
	if (selectedVal == "none") {
	    node.style("stroke", "white").style("stroke-width", "1");
	} else {
	    var selected = node.filter(function (d, i) {
	        return d.name != selectedVal;
	    });
	    selected.style("opacity", "0");
	    var link = svg.selectAll(".link")
	    link.style("opacity", "0");
	    d3.selectAll(".node, .link").transition()
	        .duration(5000)
	        .style("opacity", 1);
	}
}
