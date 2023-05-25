 
 

 
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

