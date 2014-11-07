  document.getElementById("mylink").onclick = function()
    {
        //alert("hello");
        var x = document.getElementsByTagName('tr');
        for(var i = 0; i < x.length; i++)
        {
            var str = x[i].className;
            if(str === "odd" || str === "even")
            {
                //alert("detected even odd");
                var link = x.item(i).getElementsByTagName('a')[0];
                var str = link.toString();
                document.getElementById("addhere").innerHTML = document.getElementById("addhere").innerHTML + "<p>" + str + "</p>"
            }
        }
    };
//$.get("banner.html", function (data) {
  //                  $("#appendToThis").append(data);
    //            });

