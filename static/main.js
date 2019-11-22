
var L;
      window.onload = function() {
        L.mapquest.key = 'S0grzG7xCadl79dGcxX8ZKG05uAxHTlD';
        // 'map' refers to a <div> element with the ID map
        var map = L.mapquest.map('map', {
          center: [53.480759, -2.242631],
          // 1. change 'map' to 'hybrid', try other type of map
          layers: L.mapquest.tileLayer('hybrid'),
          zoom: 12
        });
        // 2. Add control
        map.addControl(L.mapquest.control());
        // 3. Add icon
        L.marker([53.480759, -2.242631], {
          icon: L.mapquest.icons.marker({
            primaryColor: '#22407F',
            secondaryColor: '#3B5998',
            shadow: true,
            size: 'md',
            symbol: 'A'
          })
        })
        .bindPopup('This is Manchester!')
        .addTo(map);
      }


      function makepayment(key, email, amount, ref, callback) {
        var handler = PaystackPop.setup({
          key: key, // This is your public key only! 
          email: email || 'customer@email.com', // Customers email
          amount: amount || 5000000.00, // The amount charged, I like big money lol
          ref: ref || 6019, // Generate a random reference number and put here",
          metadata: { // More custom information about the transaction
           custom_fields: [
            {}
           ]
          },
          callback: callback || function(response){
            let div = document.getElementsByTagName("div")[0] 
            div.innerHTML = "This was the json response reference </br />" + response.reference;
          },
          onClose: function(){
            alert('window closed');
          }
        });
        // Payment Request Just Fired  
        handler.openIframe(); 
      }