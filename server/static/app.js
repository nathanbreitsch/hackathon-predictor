$(function(){
  function ViewModel(){
    var self = this;
    self.state = ko.observable("initial");
    self.description = ko.observable("");

    self.judge = function(){
      $.ajax({
        url: 'http://localhost:5000/judge/',
        type: 'POST',
        contentType:"application/json; charset=utf-8",
        data: JSON.stringify({
          description: self.description()
        }),
        success: function(data){
          console.log(data);
        },
        error: function(err){
          console.log(err);
        }
      });

    };


  }

  ko.applyBindings(new ViewModel());
});
