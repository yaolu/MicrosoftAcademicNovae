
var pi = Math.PI;

var arc = d3.svg.arc()
    .innerRadius(50)
    .outerRadius(70)
    .startAngle(45 * (pi/180)) //converting from degs to radians
    .endAngle(3) //just radians
    
//vis.attr("width", "800").attr("height", "800") // Added height and width so arc is visible
//    .append("path")
//    .attr("d", arc)
  //  .attr("fill", "red")
    //.attr("transform", "translate(400,400)"); 

function person_detail(id)
{
	var curWwwPath=window.document.location.href;
    //获取主机地址之后的目录，如： uimcardprj/share/meun.jsp
    var pathName=window.document.location.pathname;
    var pos=curWwwPath.indexOf(pathName);
    //获取主机地址，如： http://localhost:8083
    var localhostPath=curWwwPath.substring(0,pos);
	location.href = localhostPath+"/detail/"+id;
}

function show_tree(root_text) {

  var div = d3.select(".tooltip");

  var root = JSON.parse(root_text)

  function dump_obj(myObject) {  
    var s = "";  
    for (var property in myObject) {  
      s = s + "n "+property +": " + myObject[property];  
    }  
      alert(s);  
  }

  var radius = 60;
  var b_radius = 100;
  var side_length = 800;
  var svg = d3.select("#id-"+root.id).append("svg")  
        .attr("width", side_length)  
        .attr("height", side_length)  
        .append("g")  
        .attr("transform", "translate("+side_length/2+","+side_length/2+")");

  var tree_a = d3.layout.tree()  
         .size([360, b_radius])
         .separation(function(a, b) { return (a.distance == b.distance ? 2 : 0.5)/b.distance; });

  temp_r = {} 
  $.extend(temp_r, root)
  temp_r.children = temp_r.work_together

  var nodes = tree_a.nodes(temp_r);
  
  var links = tree_a.links(nodes);

  var link = svg.selectAll(".link")
            .data(links)
            .enter()
            .append("line")
            .attr("class", "link")
            .style("stroke", function(d) {return "rgb(0,0,0)";} )
            .style("stroke-width" , function(d) {return d.target.together_num*2;} )
            .style("stroke-opacity", 0.15)
            .attr("x1", function(d) {return 0;}  )
            .attr("y1", function(d)  {return  0; })
            .attr("x2", function(d) {return Math.cos((d.target.rr*360-90)/360*pi*2) *d.target.y*d.target.distance } )
            .attr("y2", function(d) {return  Math.sin( (d.target.rr*360-90)/360*pi*2) *d.target.y*d.target.distance } );  


  var arc3 = d3.svg.arc()
		    .innerRadius(radius/0.618+12)
		    .outerRadius(radius/0.618+18)
		    .startAngle( function(d) {  return (d.target.rr*360)/360*pi*2-0.2 } ) //converting from degs to radians
		    .endAngle( function(d) { return (d.target.rr*360)/360*pi*2+0.2 } )

  svg.selectAll(".arc")
            .data(links)
            .enter()
            .append("path")
            .attr("d", arc3)
		    .attr("fill", "#ccc");



	            
  var node = svg.selectAll(".node")  
            .data(nodes)
            .enter()
            .append("g")  
            .attr("class", "node")
            .attr("transform", function(d) { return "rotate(" + (d.rr*360-90) + ")translate("+(d.distance*d.y)+")"; });
   
 

  var arc1 = d3.svg.arc()
		    .innerRadius(68)
		    .outerRadius(70)
		    .startAngle( function(d) { return 2*pi - Math.min(d.top_num/10.0*pi+0.1, 2*pi) }) //converting from degs to radians
		    .endAngle( pi*2 );

   node.append("path")
    .attr("d", arc1)
    .attr("fill", "red")
    .attr("transform", function(d) { return "rotate(" + (-d.rr*360+90 ) + ")"; });

  var arc2 = d3.svg.arc()
		    .innerRadius(78)
		    .outerRadius(80)
		    .startAngle( function(d) { return 2*pi - Math.min(d.normal_num/10.0*pi+0.1, 2*pi) } ) //converting from degs to radians
		    .endAngle( 2*pi )

   node.append("path")
    .attr("d", arc2)
    .attr("fill", "green")
    .attr("transform", function(d) { return "rotate(" + (-d.rr*360+90 ) + ")"; });


   svg.append("circle")
	  .attr("r",radius/0.618+12)
	  .style("fill","#FCFCFC")
	  .style("stroke","#FCFCFC")
	  .style("stroke-opacity",0.2);

  node.append("circle")
  .attr("r", function(d) { return d.size*1.2;   })
  .style("fill", function(d) { return d.color;})
  .style("opacity", function(d) { return d.hasOwnProperty("name")? 0.9:0.7 } )
  .style("cursor", "pointer")
  .on("click", function(d){ person_detail(d.id) }) 
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


  



  var tree = d3.layout.tree()  
         .size([360, radius])
         .separation(function(a, b) { return (a.distance == b.distance ? 2 : 0.5)/b.distance; });

  var diagonal = d3.svg.diagonal.radial()
         .projection(function(d) {return d.hasOwnProperty("distance") ?[d.distance*d.y, (d.rr*360)/180*Math.PI]:[d.y, d.x/180*Math.PI]; });
      
  


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

  var nodes1 = tree.nodes(root);

  var links = tree.links(nodes1);

  var link = svg.selectAll(".link2")
            .data(links)
            .enter()
            .append("path")
            .attr("class", "link")
            .style("stroke", function(d) {return d.target.color;} )
            .style("stroke-opacity", 0.15)
            .attr("d",diagonal);
            
  var node = svg.selectAll(".node2")  
            .data(nodes1)
            .enter()
            .append("g")  
            .attr("class", "node")
            .attr("transform", function(d) { return "rotate(" + (d.rr*360-90) + ")translate("+(d.distance*d.y)+")"; });
 


  node.append("circle")
  .attr("r", function(d) { return d.size*1.2;   })
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


function start_search(command)
{	
	var curWwwPath=window.document.location.href;
    //获取主机地址之后的目录，如： uimcardprj/share/meun.jsp
    var pathName=window.document.location.pathname;
    var pos=curWwwPath.indexOf(pathName);
    //获取主机地址，如： http://localhost:8083
    var localhostPath=curWwwPath.substring(0,pos);

	window.location.href=encodeURI(localhostPath+'/search?command='+ command);
}

