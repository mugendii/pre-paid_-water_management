let autocomplete;

function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("id_address"),
    {
      types: ["geocode", "establishment"],
      //default in this app is Kenya only
      componentRestrictions: { country: "ke" },
    }
  );
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  let place = autocomplete.getPlace();

  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById("id_address").placeholder = "Start typing...";
  } else {
    // console.log('place name=>', place.name)
  }

  // get the address components and assign them to the fields
  // console.log(place);
  let geocoder = new google.maps.Geocoder();
  let address = document.getElementById("id_address").value;

  geocoder.geocode({ address: address }, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      let latitude = results[0].geometry.location.lat();
      let longitude = results[0].geometry.location.lng();

      // console.log('lat=>', latitude);
      // console.log('long=>', longitude);
      $("#id_latitude").val(latitude);
      $("#id_longitude").val(longitude);

      $("#id_address").val(address);
    }
  });

  // loop through the address components and assign other address data
  console.log(place.address_components);
  for (let i = 0; i < place.address_components.length; i++) {
    for (let j = 0; j < place.address_components[i].types.length; j++) {
      // get country
      if (place.address_components[i].types[j] == "country") {
        $("#id_country").val(place.address_components[i].long_name);
      }
      // get county
      if (
        place.address_components[i].types[j] == "administrative_area_level_1"
      ) {
        $("#id_county").val(place.address_components[i].long_name);
      }
      // get city
      if (place.address_components[i].types[j] == "locality") {
        $("#id_city").val(place.address_components[i].long_name);
      }
      // get postal code
      if (place.address_components[i].types[j] == "postal_code") {
        $("#id_postal_code").val(place.address_components[i].long_name);
      } else {
        $("#id_postal_code").val("");
      }
    }
  }
}

$(document).ready(function () {
  $(".add_hour").click(function (e) {
    e.preventDefault();

    let day = $("#id_day").val();
    let from_hour = $("#id_from_hour").val() || null;
    let to_hour = $("#id_to_hour").val() || null;
    let is_closed = $("#id_is_closed").is(":checked");
    let csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    let url = document.getElementById("add_hour_url").value;
    console.log(day, from_hour, to_hour, is_closed, csrf_token);

    if (is_closed) {
      is_closed = "True";
      condition = "day !=''";
    } else {
      is_closed = "False";
      condition = "day !='' && from_hour !='' && to_hour !=''";
    }
    if (eval(condition)) {
      $.ajax({
        type: "POST",
        url: url,
        data: {
          day: day,
          from_hour: from_hour,
          to_hour: to_hour,
          is_closed: is_closed,
          csrfmiddlewaretoken: csrf_token,
        },
        success: function (response) {
          let html;
          if (response.status == "success") {
            if (response.is_closed === "Closed") {
              html =
                "<tr><td class='border px-4 py-2'>" +
                response.day +
                "</td><td class='border px-4 py-2'>" +
                response.is_closed +
                "</td><td class='border px-4 py-2'>" +
                response.is_closed +
                "</td><td class='border px-4 py-2'>Delete</td></tr>";
            } else {
              html =
                "<tr><td class='border px-4 py-2'>" +
                response.day +
                "</td><td class='border px-4 py-2'>" +
                response.from_hour +
                "</td><td class='border px-4 py-2'>" +
                response.to_hour +
                "</td><td class='border px-8 py-4 font-bold text-red-500 rounded hover:text-red-700'>Delete</td></tr>";
            }

            $(".hours_table").append(html);
            $("#id_day").val("");
            $("#id_from_hour").val("");
            $("#id_to_hour").val("");
            $("#id_is_closed").prop("checked", false);
            swal("Success!", "Hours added successfully", "success");
          } else {
            swal("Error!", "Please fill all the fields", "error");
          }
        },
        error: function (response) {
          console.log(response);
        },
      });
    } else {
      swal("Error!", "Please fill all the fields", "error");
    }
  });
});

$(document).ready(function () {
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();
    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    data = {
      food_id: food_id,
    };
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        if (response.status == "Failed") {
          swal("Error!", response.message, "error");
        } else if (response.status == "login_required") {
          swal("Error!", response.message, "error").then(function () {
            window.location.href = "/accounts/login";
          });
        } else {
          swal("Success!", response.message, "success");
          $("#cart-counter").html(response.cart_counter.cart_count);
          $("#qty-" + food_id).html(response.qty);

          applyCartAmounts(
            response.cart_amounts["subtotal"],
            response.cart_amounts["tax_dict"],
            response.cart_amounts["grand_total"]
          );
        }
      },
    });
  });

  $(".item-qty").each(function () {
    let id = $(this).attr("id");
    let qty = $(this).attr("data-qty");
    $("#" + id).html(qty);
  });

  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();
    let food_id = $(this).attr("data-id");
    let cart_id = $(this).attr("id");
    let url = $(this).attr("data-url");
    let data = {
      food_id: food_id,
    };
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        if (response.status == "Failed") {
          swal("Error!", response.message, "error");
        } else {
          swal("Success!", response.message, "success");

          $("#cart-counter").html(response.cart_counter.cart_count);
          $("#qty-" + food_id).html(response.qty);

          removeCartItem(response.qty, cart_id);
          checkEmptyCart();

          applyCartAmounts(
            response.cart_amounts["subtotal"],
            response.cart_amounts["tax_dict"],
            response.cart_amounts["grand_total"]
          );

          // subtotal and total
        }
      },
    });
  });

  // Delete cart item
  $(".delete_cart").on("click", function (e) {
    e.preventDefault();
    let cart_id = $(this).attr("data-id");
    let url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,

      success: function (response) {
        if (response.status == "Failed") {
          swal("Error!", response.message, "error");
        } else {
          $("#cart-counter").html(response.cart_counter.cart_count);
          swal("Success!", response.message, "success");
          removeCartItem(0, cart_id);
          checkEmptyCart();
          applyCartAmounts(
            response.cart_amounts["subtotal"],
            response.cart_amounts["tax_dict"],
            response.cart_amounts["grand_total"]
          );

        }
      },
    });
  });

  function removeCartItem(cartItemQty, cart_id) {
    if (window.location.pathname == "/cart/") {
      if (cartItemQty <= 0) {
        document.getElementById("cart-item-" + cart_id).remove();
      }
    }
  }

  function checkEmptyCart() {
    let cart_counter = document.getElementById("cart-counter").innerHTML;
    if (window.location.pathname == "/cart/") {
      if (cart_counter == 0) {
        document.getElementById("empty_cart").style.display = "block";
      }
    }
  }

  function applyCartAmounts(subtotal, tax_dict, grand_total) {
    console.log(subtotal, tax_dict, grand_total);
    if (window.location.pathname == "/cart/") {
      $("#subtotal").html(subtotal);
      $("#grand_total").html(grand_total);

      console.log(tax_dict);
      for (key1 in tax_dict) {
        console.log(tax_dict[key1]);
        for (key2 in tax_dict[key1]) {
          console.log(tax_dict[key1][key2]);
          $("#tax-" + key1).html(tax_dict[key1][key2]);
        }
      }
    }
  }


});