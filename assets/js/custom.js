function next(){-1==window.location.search.indexOf("men")?$.get("display?gender=0",function(e){document.getElementById("content").innerHTML=e}):$.get("display?gender=1",function(e){document.getElementById("content").innerHTML=e})}function like(){$("#itemdisplay").animate({height:"0px",left:"250px",opacity:"0.0"});setTimeout(function(){next()},400)}function dislike(){$("#itemdisplay").animate({height:"0px",right:"250px",opacity:"0.0"});setTimeout(function(){next()},400)}function buy(e){$("#itemdisplay").animate({down:"250px",opacity:"0.0"});setTimeout(function(){window.open("http://offer.ebay.com/ws/eBayISAPI.dll?BinConfirm&item="+e,"","width=1000, height=750, top="+(screen.height/2-375)+", left="+(screen.width/2-500));next()},400)}function fade(){$("#homecontent").animate({opacity:"0.0"})}function goSwipe(){fade();setTimeout(function(){window.location.assign("swipe")},400)}function go(){fade();setTimeout(function(){window.location.assign("swipe?men")},400)}