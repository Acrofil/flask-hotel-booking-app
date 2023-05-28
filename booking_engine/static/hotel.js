
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

    $('.dates_rate_plans #start_date_1, #start_date_2, #start_date_3, #start_date_4').datepicker({
        'format': 'dd-mm-yyyy', 'todayHighlight': true, 'showOnFocus': true, 'startDate': '0',
        'autoclose': true
        
    });

     

    $('.dates_rate_plans #end_date_1, #end_date_2, #end_date_3, #end_date_4').datepicker({
        'format': 'dd-mm-yyyy', 'todayHighlight': true, 'showOnFocus': true, 'startDate': '0',
        'autoclose': true
    });
    

});
