const elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

const form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
ev.preventDefault();



  $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: {
      order_key: clientsecret,
      action: "post",
    },
    success: function (json) {
      console.log(json.success)
     },
    error: function (xhr, errmsg, err) {},
  });
});