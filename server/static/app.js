$(function(){
  function ViewModel(){
    var self = this;
    self.state = ko.observable("initial");
    self.description = ko.observable("");
    self.scatterData = ko.observableArray();
    self.winners = [];
    self.losers = [];

    self.judge = function(){
      $.ajax({
        url: 'http://localhost:5000/judge/',
        type: 'POST',
        contentType:"application/json; charset=utf-8",
        data: JSON.stringify({
          description: self.description()
        }),
        success: function(data){
          if(data.result == 1){
            self.state("winner");
          }
          else{
            self.state("loser");
          }
        },
        error: function(err){
          console.log(err);
        }
      });

    };

    $.ajax({
      url: '/scatter/',
      type: 'GET',
      success: function(data){
        projects = data.data;
        winners = projects.filter(function(d){return d.w == 1;})
                      .map(function(d){return [d.x, d.y]})

        losers = projects.filter(function(d){return d.w == 0;})
                      .map(function(d){return [d.x, d.y]})

        self.winners = winners;
        self.losers = losers;

        console.log(winners);
        self.scatterData(data.data);
        //console.log(self.scatterData());
      }
    });


    self.drawScatter = function(){


      $('#plot').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: "Principle Components"
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            title: {
                text: "PC1"
            }
        },
        yAxis: {
            title: {
                text: "PC2"
            }
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                }
            }
        },
        series: [
        /*  {
          name: 'Projects',
          turboThreshold: 100000,
          data: self.scatterData().map(function(d){
            //d.color = "#00FF00";
            return d;
          })
        }*/
        {
          name: 'Winners',
          data: self.winners
        },
        {
          name: 'Non-Winners',
          data: self.losers
        }
      ]
    });


      self.state('plot');
    };


  }

  ko.applyBindings(new ViewModel());
});
