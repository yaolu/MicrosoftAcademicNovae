function show_tree(root_text) {
  var drag = d3.behavior.drag()
            .on("drag", dragmove); 
            
  function dragmove(d) {  
    d3.select(this)
      .attr("cx", d.cx = d3.event.x )
      .attr("cy", d.cy = d3.event.y );
  }

  var div = d3.select(".tooltip");

  var root = JSON.parse(root_text)

  function dump_obj(myObject) {  
    var s = "";  
    for (var property in myObject) {  
      s = s + "n "+property +": " + myObject[property];  
    }  
      alert(s);  
  }
  var radius = 45;

  var tree = d3.layout.tree()  
         .size([360, radius])
         .separation(function(a, b) { return (a.distance == b.distance ? 2 : 0.5)/b.distance; });

  var diagonal = d3.svg.diagonal.radial()
         .projection(function(d) {return d.hasOwnProperty("distance") ?[d.distance*d.y, (d.rr*360)/180*Math.PI]:[d.y, d.x/180*Math.PI]; });
      
  var svg = d3.select("#id-"+root.id).append("svg")  
        .attr("width", radius*4.0)  
        .attr("height", radius*4.0)  
        .append("g")  
        .attr("transform", "translate("+radius*2.0+","+radius*2.0+")");

  svg.append("circle")
  .attr("r",radius)
  .style("stroke-dasharray", ("5, 5"))
  .style("fill","none")
  .style("stroke","black")
  .style("stroke-opacity",0.2);

  svg.append("circle")
  .attr("r",radius/0.618)
  .style("stroke-dasharray", ("5, 5"))
  .style("fill","none")
  .style("stroke","black")
  .style("stroke-opacity",0.2);

  svg.append("line")
  .style("stroke-dasharray", ("5, 5"))
  .style("fill","none")
  .style("stroke","black")
  .style("stroke-opacity",0.2)
  .attr("x1", 0)
  .attr("y1", 0)
  .attr("x2", 0)
  .attr("y2", -radius/0.570);





  var nodes = tree.nodes(root);
  var links = tree.links(nodes);

  var link = svg.selectAll(".link")
            .data(links)
            .enter()
            .append("path")
            .attr("class", "link")
            .style("stroke", function(d) {return d.target.color;} )
            .style("stroke-opacity", 0.15)
            .attr("d",diagonal);
            
  var node = svg.selectAll(".node")  
            .data(nodes)
            .enter()
            .append("g")  
            .attr("class", "node")
            .attr("transform", function(d) { return "rotate(" + (d.rr*360-90) + ")translate("+(d.distance*d.y)+")"; });


  node.append("circle")
  .attr("r", function(d) { return d.size;   })
  .style("fill", function(d) { return d.color;})
  .style("opacity", function(d) { return d.hasOwnProperty("name")?0.9:0.7 } )

  .on("mouseover", function(d) {      
            div.transition()        
                .duration(200)      
                .style("opacity", .9);      
            div .html(d.description)  
                .style("left", (d3.event.pageX + 50) + "px")     
                .style("top", (d3.event.pageY ) + "px");    
            })                  
  .on("mouseout", function(d) {       
            div.transition()        
                .duration(500)      
                .style("opacity", 0);   
        });

  /*node.append("text")  
      .attr("dx", function(d) { return d.children ? -30 : 30; })
      .attr("dy", 20)
      .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
      .text(function(d) { return d.description; });  
  */
};