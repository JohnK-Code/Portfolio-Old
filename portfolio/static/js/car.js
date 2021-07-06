document.addEventListener('DOMContentLoaded', function(){

    // Code for Swiper JS Initialization 
    var swiper = new Swiper(".swiper-container", {
        breakpoints: {
            640: {
                slidesPerView: 1,
                spaceBetween: 50,
                slidesPerGroup: 1,
            },
            768: {
                slidesPerView: 2,
                spaceBetween: 40,
                slidesPerGroup: 1,
            },
            1024: {
                slidesPerView: 3,
                spaceBetween: 30,
                slidesPerGroup: 1
            }
        },
        loop: true,
        loopFillGroupWithBlank: true,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      });


      // Code for ajax form GET request - Used to update the Car Model field using Manufacturer field Info.
      $("#car_make").change(function(e){  // Used to update the 'model' field in the form when a 'manufacturer' is selected - No page reload required.
        e.preventDefault();   
        // Get car make
        var car_make = $(this).children("option:selected").val();
        // GET ajax request
        $.ajax({
            type:'GET',
            url: $(this).data('url'),
            data: {"car_make": car_make},
            success: function(data) { // Handle response
                $('#car_model option').remove()
                $('#car_model').append(`<option value>Model</option>`) // value in option element is important and stops form working without it
                $.each(data, function(index, model){
                    $('#car_model').append(`<option value="${model}">${model}</option>`)
                })
            }
        })
    })
    

})