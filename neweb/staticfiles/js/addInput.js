var counter = 1;
var limit = 3;
function addInput(divName){
          var newdiv = document.createElement('div');
          newdiv.innerHTML = document.getElementById('fooditem').value+"'s Quantity<br><input type='number' name='itemNum' class='validate' required='' aria-required='true'> <input type='hidden' id='foodname' name='foodname' value = '"+document.getElementById('fooditem').value+"'>";
          document.getElementById(divName).appendChild(newdiv);

          counter++;
};

function addInfo(divName){
          var newdiv = document.createElement('div');
          newdiv.innerHTML = document.getElementById('fooditem').value+"'s Quantity<br><input type='number' name='itemNum' class='validate' required='' aria-required='true'> <input type='hidden' id='foodname' name='foodname' value = '"+document.getElementById('fooditem').value+"'>";
          document.getElementById(divName).appendChild(newdiv);

          counter++;
}
