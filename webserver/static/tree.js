function show_tree(root_text) {
  var root = JSON.parse(root_text)
  console.log( root_text ); 
  function dump_obj(myObject) {  
    var s = "";  
    for (var property in myObject) {  
      s = s + "n "+property +": " + myObject[property];  
    }  
      alert(s);  
  }
  var width = 400;
  var height = 400;

  var tree = d3.layout.tree()  
         .size([360, 360])
         .separation(function(a, b) { return (a.distance == b.distance ? 2 : 0.5)/b.distance; });

  var diagonal = d3.svg.diagonal.radial()
         .projection(function(d) {return d.hasOwnProperty("distance") ?[d.distance*d.y/5, (d.rr+d.x)/180*Math.PI]:[d.y/4, d.x/180*Math.PI]; });
  var diagonal = d3.svg.line.radial()
        .radius("radius", 10 )
        .angle("angle", 10 );
      
  var svg = d3.select("#relevanceRuleConfig").append("svg")  
        .attr("width", width)  
        .attr("height", height)  
        .append("g")  
        .attr("transform", "translate(200,200)");

  var nodes = tree.nodes(root);
  var links = tree.links(nodes);

  var link = svg.selectAll(".link")
            .data(links)
            .enter()
            .append("line")
            .attr("class", "link")
            .style("stroke", function(d) {return d.target.color;} )
            .style("stroke-opacity", 0.2)
            .style("stroke-width" , "100" )
            .attr("x1", function(d) {return  d.source.distance*d.source.y/5 ;}  )
            .attr("y1", function(d)  {return  d.source.x-180 }   )
            .attr("x2", function(d) {return Math.cos((d.target.rr+ d.target.x-90)/180*Math.PI)*d.target.y/5*d.target.distance } )
            .attr("y2", function(d) {return  Math.sin( (d.target.rr+d.target.x-90)/180*Math.PI)*d.target.y/5*d.target.distance } );  

  var node = svg.selectAll(".nodep")  
            .data(nodes)
            .enter()
            .append("g")  
            .attr("class", "nodep")
            .attr("transform", function(d) { return "rotate(" + (d.rr+d.x-90) + ")translate("+(d.distance*d.y/5)+")"; });


  node.append("circle")
  .attr("r", function(d) { return d.size;   })
  .style("fill", function(d) { return d.color;} );  


  node.append("text")  
      .attr("dx", function(d) { return d.children ? -8 : 8; })
      .attr("dy", 3)
      .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
      .text(function(d) { return d.name; });  

};