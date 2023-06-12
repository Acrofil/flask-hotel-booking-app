
    // const & function for button animation
    const toggler_button = document.querySelector('.navbar-toggler')
    const drop_down = document.querySelector('.collapse')
    const button_icon = document.querySelector('.navbar-toggler-icon')
   
    toggler_button.onclick = function() {
       drop_down.classList.toggle('open')
       const isOpen = drop_down.classList.contains('open')
   
       button_icon.classList = isOpen
       ? 'fa-solid fa-xmark'
       : 'fa-solid fa-bars'
    }
 
 // function to show or hide children select forms based on how many children have been selected
 $(function toggle_display(){

    $("option").click(function() {

        // this are the targeted options initialy set to hidden
        one_child = document.querySelector('.one_child')
        two_children = document.querySelector('.two_children')

        // returns the number of children selected
        var total_children = $(this).val();
 
        
        if(total_children == 'one'){
            one_child.style.display = 'block'
            two_children.style.display = 'none'
            $('.required1').prop('required', true);

        }
        else if (total_children == 'two'){
            one_child.style.display = 'block'
            two_children.style.display = 'block'

            $('.required1').prop('required', true);
            $('.required2').prop('required', true);
        }
        else if (total_children == 'none') {

            one_child.style.display = 'none'
            two_children.style.display = 'none'

        }
        
    });


    // Function to show or hide different date periods in Rate Plans section
    let val = 0
    $(document).on('click', '#add_rate_plan, #remove_rate_plan', function(){ 


            // Target classes
            period_2 = document.querySelector('.period_two')
            period_3 = document.querySelector('.period_three')
            period_4 = document.querySelector('.period_four')
        
            var on_button_click = $(this).val();

            // if add or remove 
            if(on_button_click == 'add'){
                val += 1
    
                if(val > 3){
                    val -= 1
                }
            }
            else if(on_button_click == 'remove'){
                val -= 1
                
                if(val < 0){
                    val += 1
                }
            }
            
                if(val == 1){
                    period_2.style.display = 'block'
                    period_3.style.display = 'none'
                    period_4.style.display = 'none'
    
                    $('.requered_rate_plan2').prop('required', true);
                }
                else if(val == 2){
                    period_4.style.display = 'none'
                    period_3.style.display = 'block'
                    $('.requered_rate_plan3').prop('required', true);
                    
                }
                else if(val == 3){
                    period_4.style.display = 'block'
                    $('.requered_rate_plan4').prop('required', true);
                }
                else if(val == 0){
                    period_2.style.display = 'none'
                    period_3.style.display = 'none'
                    period_4.style.display = 'none'
                    $('.requered_rate_plan2').prop('required', false);
                    $('.requered_rate_plan3').prop('required', false);
                    $('.requered_rate_plan4').prop('required', false);
    
                }
                ;
    });

});


// hiding each rate plan
$(document).ready(function(){
	$('#show1, #hide1').on('click',function(){	
		$('.hide_row1').toggle();
	});
});

$(document).ready(function(){
	$('#show2, #hide2').on('click',function(){	
		$('.hide_row2').toggle();
	});
});

$(document).ready(function(){
	$('#show3, #hide3').on('click',function(){	
		$('.hide_row3').toggle();
	});
});

$(document).ready(function(){
	$('#show4, #hide4').on('click',function(){	
		$('.hide_row4').toggle();
	});
});

$(document).ready(function(){
	$('#show5, #hide5').on('click',function(){	
		$('.hide_row5').toggle();
	});
});

// for the datepicker calendar
    $(function() {

    $('.dates #checkin').datepicker({
        'format': 'dd-mm-yyyy', 'todayHighlight': true, 'showOnFocus': true, 'startDate': '0',
        'autoclose': true
        
    });

     

    $('.dates #checkout').datepicker({
        'format': 'dd-mm-yyyy', 'todayHighlight': true, 'showOnFocus': true, 'startDate': '0',
        'autoclose': true
    });
    

});

// for the datepicker calendar in rate plans
$(function() {

    $('.dates_rate_plans #from_date, #start_date, #start_date_1, #start_date_2, #start_date_3, #start_date_4').datepicker({
        'format': 'dd-mm-yyyy', 'todayHighlight': true, 'showOnFocus': true, 'startDate': '0',
        'autoclose': true
        
    });

     

    $('.dates_rate_plans #to_date, #end_date, #end_date_1, #end_date_2, #end_date_3, #end_date_4').datepicker({
        'format': 'dd-mm-yyyy', 'todayHighlight': true, 'showOnFocus': true, 'startDate': '0',
        'autoclose': true
    });
    

});

// does nothing for now
$(document).ready(function(){
    $("form[name='availability_form']").submit(function(event) {
      event.preventDefault();
      $.post("/greet", $(this).serialize())
        .done(function(data) {
          $("#message").html(data.message);
        })
        .fail(function() {
          $("#message").html("An error has occurred.");
        });
    });
  });

  

    

let table = new DataTable('#reservations');
$(document).ready(function () {
    $('#example').DataTable();
});


  // Get dict data from selecting rooms offer / offer_rooms.html

  $.ajax({
    url: "/booking_request",
    type: "POST",
    contentType: "application/json;charset=UTF-8",
    dataType: "json",
    data: JSON.stringify({html_data: bookable_rooms}),
    success: function(response) {
        console.log(response);
    },

  });

  (function () {
    'use strict'
    const forms = document.querySelectorAll('.requires-validation')
    Array.from(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
    
          form.classList.add('was-validated')
        }, false)
      })
    })()