(function() {
  var box, color, currentDataset, force, getSvgBox, graph, lastChoice, last_detail_node, link, links, loaded, node, nodes, setMetaAnchor, showDetail, showLink, svg, update, years;

  color = d3.scale.category10()

  getSvgBox = function() {
    var el;
    el = document.querySelector('#svg-wrap');
    return el.getBoundingClientRect();
  };

  svg = d3.select("#main-view");

  box = getSvgBox();

  force = d3.layout.force().charge(-900).linkDistance(100).size([box.width, box.height]).alpha(1);

  graph = null;

  links = force.links();

  nodes = force.nodes();

  link = svg.selectAll(".link");

  node = svg.selectAll(".node");

  currentDataset = null;

  years = null;

  last_detail_node = 5;

  showLink = function(data) {
    var html;
    html = '';
    if (data) {
      html += '<table>';
      html += '<tr>';
      html += "<th>From</th>";
      html += "<td>" + data.source.name + "</td>";
      html += '</tr>';
      html += '<tr>';
      html += "<th>To</th>";
      html += "<td>" + data.target.name + "</td>";
      html += '</tr>';
      html += '<tr>';
      html += "<th>Weight</th>";
      html += "<td>" + (data.rate || 0) + "</td>";
      html += '</tr>';
      html += '</table>';
    }
    return (document.getElementById('explaination-link')).innerHTML = html;
  };

  showDetail = function(data) {
    var html;
    last_detail_node = data.index;
    html = '<table>';
    html += '<tr>';
    html += "<th>Category</th>";
    html += "<td>" + data.category + "</td>";
    html += '</tr>';
    html += '<tr>';
    html += "<th>Name</th>";
    html += "<td>" + data.name + "</td>";
    html += '</tr>';
    html += '<tr>';
    html += "<th>Weight</th>";
    html += "<td>" + (data.rate || 0) + "</td>";
    html += '</tr>';
    html += '</table>';
    return (document.getElementById('explaination-node')).innerHTML = html;
  };

  setMetaAnchor = function() {
    var i, offset, y, _i, _results;
    box = getSvgBox();
    nodes = currentDataset.nodes;

	/*
	y = box.height * 0.5;
	for (i = _i = 0; _i < last_detail_node; i = ++_i) {
		nodes[i].x = nodes[i].px = box.width * (i+2) / (last_detail_node+3);
	}
	for (i = _i = 0; _i < last_detail_node; i = ++_i) {
		nodes[i].y = nodes[i].py = y;
	}
	*/

	nodes[0].x = box.width / 2;
	nodes[1].x = box.width / 2;
	nodes[2].x = box.width / 2;
	nodes[3].x = box.width / 4;
	nodes[4].x = box.width * 3 / 4;
	nodes[0].y = box.height * 2 / 5;
	nodes[1].y = box.height / 2;
	nodes[2].y = box.height * 3 / 5;
	nodes[3].y = box.height / 2;
	nodes[4].y = box.height / 2;

    _results = [];
    for (i = _i = 0; _i < last_detail_node; i = ++_i) {
      _results.push(nodes[i].fixed = true);
    }
    return _results;
  };

  loaded = [];

  lastChoice = 0;

  update = function(_index) {
    var cur, d, i, key, last, nodeG, priority, s, year, _i, _j, _len, _ref, _ref1;
    (document.getElementById('year-title')).innerText = years[_index];
    year = years[_index];
    last = graph[years[lastChoice]];
    lastChoice = _index;
    cur = currentDataset = graph[year];
    for (i = _i = 0, _ref = last.nodes.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
      d = cur.nodes[i];
      s = last.nodes[i];
      _ref1 = ['index', 'x', 'y', 'px', 'py', 'fixed', 'weight'];
      for (_j = 0, _len = _ref1.length; _j < _len; _j++) {
        key = _ref1[_j];
        d[key] = s[key];
      }
    }
    setMetaAnchor();
    force.nodes(cur.nodes).links(cur.links).linkStrength(function(d) {
      if (d.rate) {
        return d.rate / 200;
      }
      return .1;
    }).linkDistance(function(d) {
      if (d.type === "inner") {
        return 50;
      } else if (d.type === "outer") {
        return 400;
      } else {
        return 10;
      }
    });
    if (!loaded[_index]) {
      force.start();
      loaded[_index] = true;
    } else {
      force.resume();
    }
    showDetail(cur.nodes[last_detail_node]);
    showLink();
    link = svg.selectAll(".link").data(cur.links);
    link.enter().append("line").attr("class", function(d) {
      switch (d.type) {
        case "inner":
        case "outer":
          return "link";
        case "metalink":
          return "metalink link";
        default:
          throw 'not support type';
      }
    });
    link.exit().remove();
    link.transition().duration(850).style("stroke-width", function(d) {
      if (d.rate) {
        return Math.sqrt(d.rate) / 2;
      }
      return 2;
    }).attr("class", function(d) {
      switch (d.type) {
        case "inner":
        case "outer":
          return "link";
        case "metalink":
          return "metalink link";
        default:
          throw 'not support type';
      }
    });
    node = svg.selectAll(".node").data(cur.nodes, function(d) {
      return d.index;
    });
    nodeG = node.enter().append("g").attr("class", function(d) {
      switch (d.type) {
        case "normal":
          return "node";
        case "meta":
          return "meta node";
        default:
          throw 'not support type';
      }
    }).call(force.drag);
    nodeG.append("circle").attr("r", 10).style("opacity", 1);
    nodeG.append("text").attr("dy", ".35em").style("text-anchor", "middle").text(function(d) {
      return d.name;
    });
    nodeG.append("title").text(function(d) {
      return d.name;
    });
    node.exit().remove();
    node.transition().duration(350).select("circle").attr("r", function(d) {
      if (d.type === "meta") {
        return 10;
      }
      if (d.rate) {
        return d.rate * 50;
      } else {
        return 1;
      }
    }).style("opacity", function(d) {
      if (d.type === "meta") {
        return 0.2;
      } else {
        if (d.rate) {
          return 1;
        } else {
          return 0.5;
        }
      }
    }).attr("fill", function(d) {
      return color(d.category);
    });
	node.transition().duration(350).select("text").text(function(d) {
      return d.name;
    });
    node.on('mouseenter', function(d) {
      return showDetail(d);
    });
    link.on('mouseenter', function(d) {
      var _ref2;
      if ((_ref2 = d.type) === 'inner' || _ref2 === 'outer') {
        return showLink(d);
      }
    });
    priority = {
      inner: 0,
      outer: 1,
      normal: 10,
      metalink: 0
    };
    svg.selectAll(".node, .link").sort(function(a, b) {
      if (priority[a.type] > priority[b.type]) {
        return 1;
      }
      return -1;
    });
  };

  d3.json("graph.json", function(error, graphJSON) {
    var keymap, offset, scollbar;
    years = graphJSON.year_description;
    graph = graphJSON.data;
    offset = {
      affiliation: -1,
      author: -0.5,
      paper: 0,
	  venue: 0.5,
      word: 1
    };
    force.on("tick", function(e) {
      var k;
      k = 3 * e.alpha;
      currentDataset.nodes.forEach(function(o) {
        o.x += offset[o.category] * k;
      });
      link.attr("x1", function(d) {
        return d.source.x;
      }).attr("y1", function(d) {
        return d.source.y;
      }).attr("x2", function(d) {
        return d.target.x;
      }).attr("y2", function(d) {
        return d.target.y;
      });
      node.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
    });
    update(0);
    scollbar = document.getElementById('year-select');
    scollbar.onchange = function(e) {
      update(parseInt(this.value));
      return false;
    };
    keymap = {
      37: -1,
      39: +1
    };
    window.onkeydown = function(e) {
      var newValue, value;
      if (value = keymap[e.keyCode]) {
        newValue = parseInt(scollbar.value) + value;
        if ((0 <= newValue && newValue < years.length)) {
          scollbar.value = newValue;
          return update(newValue);
        }
      }
    };
    window.onresize = function(e) {
      box = getSvgBox();
      force.size([box.width, box.height]);
      return update(lastChoice);
    };
  });

}).call(this);
