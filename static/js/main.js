
      function payWithPaystack2() {
        let amt=$('#pricetopay').val()
        let amount =  Number(amt ) * 100

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
           response["price"] = amount
            let data = JSON.stringify(response)
            $.ajax({
                url: '/create_transactions',
                data:data,
                contentType: 'json',
                type: 'POST',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                success: (data) => {console.log(data); window.location = '/booked' }
               
            })
            
         
        }
    
    })
    handler.openIframe();
    }

   
function datep(){
  var today = new Date()
   let date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
        let inputDate = document.getElementById('date');
        inputDate.min = date;  
}

function myFunction(id){
    x = document.getElementById(id+"input")
    console.log(x)
    if (x.style.display == "none"){
        x.style.display = "block";
    } else {
        x.style.display="none"
    }
//   for(let i of x){
//     i.style.display="block"
//   }
}
