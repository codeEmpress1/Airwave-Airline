
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

      function payWithPaystack2() {
        let amt=$('#pricetopay').val()
        let amount =  Number(amt ) * 100
        console.log(amount)
        let email=$("#email").val()
        let phone = $("#phone").val()
        let userId = $("#userId").val()
        let fullname = $("#fullname").val()
    var handler = PaystackPop.setup({
        key: 'pk_test_2c2ac8fbaf18b0e9af6b38d1e05e95c2f1f07b67', //put your public key here
        email: email, //put your customer's email here
        amount: Number(amount),
        currency:"NGN", //amount the customer is supposed to pay
        metadata: {
            custom_fields: [
                {
                    display_name: fullname,
                    variable_name: "phone number",
                    value: phone//customer's mobile number
                }
            ]
        },
        callback: function (response) {
           // debugger;
           response["name"] = fullname;
           response["email"] = email;
           response["userId"] = userId
           response["phone"] = phone;
            let data = JSON.stringify(response)
            $.ajax({
                url: '/create_transactions',
                data:data,
                contentType: 'json',
                type: 'POST',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                success: (data) => console.log(data) 
               
            })
            
         
        }
    
    })
    handler.openIframe();
    }


    var today = new Date()
   let date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
        let inputDate = document.getElementById('date');
        inputDate.min = date;
    
