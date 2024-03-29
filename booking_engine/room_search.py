from booking_engine.models import RateType, RatePlan, RoomAvailability, Room
from flask import flash
from datetime import timedelta, datetime
from math import floor, ceil

def single_room_search(room, rooms_request, total_guests, adults, total_children, listed_rooms: list, checkin, checkout, first_child, second_child, children, total_days  ): 
    
    available = True
    no_availability = []

    days = 0
    for r in listed_rooms:
        
        if r.room_id == room.id:
            days += 1
    
    
    for listed_room in listed_rooms:
        for date in listed_room.room_availability:
            if listed_room.id == date.listed_room_id and listed_room.room_id == room.id and (date.left_to_sell - rooms_request) < 0:
                available = False
                not_available = datetime.strftime(listed_room.listed_date, "%d %m")
                no_availability.append(not_available)
            

    if available and days == total_days:            

        for listed_room in listed_rooms:

            # If there is desired room quantity available
            if listed_room.room_id == room.id:

                # Get rateplan between dates                      
                rp = (RatePlan.query.filter(RatePlan.rate_type_id == listed_room.rate_type_id).
                                filter(RatePlan.from_date <= checkin).
                                filter(checkout - timedelta(days=1) <= RatePlan.to_date).first())
                
                if rp and listed_room.listed_date == checkout - timedelta(days=1):

                    price_per_day_adults = 0
                    price_per_day_childen = 0
                    children_extra_bed = 0
                    adults_difference = 0
                    total_price = 0
                    children_on_regular_bed = 0
                    
                    # If adults are between min guests and max adults and total children + adults not exceeds max_guests
                    if adults >= room.min_guests and adults <= room.max_adults and total_children and total_children + adults <= room.max_guests:

                        # Get price per day for adults
                        price_per_day_adults = adults * rp.adult

                        # Check how many children
                        all_children = list([first_child if children == 'one' else first_child, second_child])

                        # Check each child of what age is it and add the correct price from the rateplan
                        for child in all_children:

                            if child == '7-12':
                                price_per_day_childen += rp.child_under_12_exb
                            elif child == '2-6':
                                price_per_day_childen += rp.child_under_7_exb
                            elif child == '0-2':
                                price_per_day_childen += rp.child_under_2_exb
                            
                    # For adults that are equal or more than room min guests and less or == max_guests
                    if adults >= room.min_guests and adults <= room.max_guests and not total_children:
                        price_per_day_adults = adults * rp.adult
                    
                    # For single person with room that has min guest of 1 person
                    if adults == 1 and room.min_guests == 1 and not total_children:
                        price_per_day_adults = adults * rp.single_adult
                    
                    if adults == 1 and room.min_guests == 1 and total_children != 0:
                        price_per_day_adults = adults * rp.adult
                        

                        if (room.max_adults - adults) == total_children:
                            price_per_day_childen = total_children * rp.child_under_12_rb
                        else:
    
                            price_per_day_childen = ((total_children - 1) * rp.child_under_12_rb) + ( (total_children - 1) * rp.child_under_12_exb if second_child == '7-12' else rp.child_under_7_exb if second_child == '2-6' else rp.child_under_2_exb if second_child == '0-2' else 0)
                        

                    # Offer the room for the full price even if adults are less than req minimum guests   
                    if adults < room.min_guests and total_children == 0:
                        price_per_day_adults =  rp.single_adult
                    
                    # Adults + children under 12 y.o on regular beds + exb
                    if adults < room.min_guests and total_children <= room.max_children and total_children != 0 and adults + total_children <= room.max_guests:
                        price_per_day_adults = adults * rp.adult

                        # Get the difference Example: 1 adult with 2 children - min guests = 3 - 1 adult == 2, 2 children must be taxed for regular bed
                        adults_difference = room.min_guests - adults
                        
                        end = adults_difference
                        for child in range(1, adults_difference + (1 if adults_difference == end else 0)):
                            price_per_day_childen += 1 * rp.child_under_12_rb
                            children_on_regular_bed += 1
                        
                        children_extra_bed = (total_children - children_on_regular_bed) * rp.child_under_12_exb


                    total_price_day = (price_per_day_adults + price_per_day_childen + children_extra_bed)

                    price_room_stay = total_price_day * rooms_request
                    total_price = total_price_day * total_days

                    room_option = {
                        'room_type': room.name,
                        'room_quantity': rooms_request,
                        'from_date': checkin,
                        'to_date': checkout,
                        'max_guests': room.max_guests,
                        'total_days': total_days,
                        'total_guests': total_guests,
                        'total_adults': adults,
                        'total_children': total_children,
                        'children_age': tuple([first_child, second_child]) if total_children == 2 else first_child,
                        'price_per_day': total_price_day,
                        'price_room_stay': price_room_stay,
                        'total_price': total_price,
                        'room_image': room.room_image,
                        'room_info': room.room_description

                            }
                        
                    return room_option
    

def multiple_rooms_search_no_children(room, rooms_request, total_guests, adults, listed_rooms, checkin, checkout, total_days, first_child, second_child, total_children):
      
    client_search = [(adults, rooms_request)]        

    #room_availability = RoomAvailability.query.filter(RoomAvailability.listed_room_id == listed_room.id).filter(Room.id == room.id).all()
    available = True

    days = 0
    for r in listed_rooms:
        
        if r.room_id == room.id:
            days += 1

    no_availability = []

    for listed_room in listed_rooms:
        for date in listed_room.room_availability:
            if listed_room.id == date.listed_room_id and listed_room.room_id == room.id and (date.left_to_sell - rooms_request) < 0:
                available = False
                not_available = datetime.strftime(listed_room.listed_date, "%d %m")
                no_availability.append(not_available)

    if available and days == total_days:

        room_capacity = 0
        for guests, rooms in client_search:

            capacity = guests / rooms               
            room_capacity = capacity
                
        # Loop all listed rooms for the selected dates
        for listed_room in listed_rooms:
            
            # Check if we have the requeired quantity for the selected dates
            if room.id == listed_room.room_id:
        
                rate_plan = (RatePlan.query.filter(RatePlan.rate_type_id == listed_room.rate_type_id).
                        filter(RatePlan.from_date <= checkin).
                        filter(checkout - timedelta(days=1) <= RatePlan.to_date).first())
                            
                                
                adults_price_per_day = 0
                                    
                if room.min_guests == 1 and room_capacity <= room.max_adults and room_capacity != 1:
                    adults_price_per_day = total_guests * rate_plan.adult
                    
                # If the search is for example 5 rooms and 5 persons 
                if room.min_guests == 1 and room_capacity == 1:
                    adults_price_per_day += total_guests * rate_plan.single_adult
                    
                # if the req room capacity is less than room.min_guests: Tax them with single_adult rate
                if room_capacity < room.min_guests:
                    adults_price_per_day = total_guests * rate_plan.single_adult
                    
                if room_capacity < room.min_guests and (adults / rooms_request) < room.min_guests:
                    adults_price_per_day = (room.min_guests * rate_plan.adult) * rooms_request
                    
                # If the search fits the room min and max criteria and its not for single rooms search
                if room_capacity >= room.min_guests and room_capacity <= room.max_adults and room_capacity != 1:
                    adults_price_per_day = room.min_guests * rate_plan.adult
                    
                if room_capacity >= room.min_guests and room_capacity <= room.max_adults and room_capacity != 1:
                    adults_price_per_day = total_guests * rate_plan.adult
                    
                # room_capacity is between min guests and max_adults: Tax the rooms with aduults == max_adults with regular price and tax with single_price the ones who are with less
                if room_capacity > room.min_guests and room_capacity < room.max_adults:
                    adult_difference = floor(adults / rooms_request)

                    if adult_difference < room.min_guests or adult_difference == 1:
                        adults_price_per_day = (((total_guests - adult_difference) * rate_plan.adult) + (adult_difference * rate_plan.single_adult) 
                                                    if (room.max_adults == (adults - adult_difference) and adult_difference == 1 or room.max_adults == ((total_guests - adult_difference) / room.max_adults))
                                                    else ((total_guests - (adult_difference + 1)) * rate_plan.adult) + ((adult_difference + 1) * rate_plan.single_adult))
                        
                    elif adult_difference >= room.min_guests and adult_difference < room.max_guests and adult_difference != 1:
                            adults_price_per_day = (((total_guests - adult_difference) * rate_plan.adult) + (adult_difference * rate_plan.single_adult) 
                                                    if (room.max_adults == (adults - adult_difference) and adult_difference == 1 or room.max_adults == ((total_guests - adult_difference) / room.max_adults))
                                                    else ((total_guests - (adult_difference + 1)) * rate_plan.adult) + ((adult_difference + 1) * rate_plan.adult))
                    
                    
            
                # If there is rate plan for the selected dates
                if rate_plan and listed_room.listed_date == checkout - timedelta(days=1):

                    price_per_day_room = adults_price_per_day / rooms_request
                    price_per_room_all_days = price_per_day_room * rooms_request
                    all_rooms_total = price_per_room_all_days * total_days

                    room_option = {
                        'room_type': room.name,
                        'room_quantity': rooms_request,
                        'from_date': checkin,
                        'to_date': checkout,
                        'total_days': total_days,
                        'max_guests': room.max_guests,
                        'total_guests': total_guests,
                        'total_adults': adults,
                        'total_children': 0,
                        'children_age': tuple([first_child, second_child]) if total_children == 2 else first_child,
                        'price_per_day': price_per_day_room,
                        'price_room_stay': price_per_room_all_days,
                        'total_price': all_rooms_total,
                        'room_image': room.room_image,
                        'room_info': room.room_description

                        }                      

                    return room_option
    

def multiple_rooms_search_children(room, rooms_request, total_guests, adults, total_children, listed_rooms: list, checkin, checkout, first_child, second_child, children, total_days):
    
    available = True
    no_availability = []

    days = 0
    for r in listed_rooms:
        
        if r.room_id == room.id:
            days += 1
    
    for listed_room in listed_rooms:

        for date in listed_room.room_availability:
            if listed_room.id == date.listed_room_id and listed_room.room_id == room.id and (date.left_to_sell - rooms_request) < 0:
                available = False
                not_available = datetime.strftime(listed_room.listed_date, "%d %m")
                no_availability.append(not_available)
    
    if available and days == total_days:

        for listed_room in listed_rooms:
        
            # Check if we have the requeired quantity for the selected dates
            if  (room.id == listed_room.room_id and total_guests <= (room.max_guests * rooms_request)): 

                adults_price = 0
                children_price = 0
                children_on_regular_bed = 0

                # Get rateplan between dates                      
                rp = (RatePlan.query.filter(RatePlan.rate_type_id == listed_room.rate_type_id).
                        filter(RatePlan.from_date <= checkin).
                        filter(checkout - timedelta(days=1) <= RatePlan.to_date).first())
            
                # Tax all adults regular price and all children extra bed price
                if adults >= (room.min_guests * rooms_request) and adults <= (room.max_adults * rooms_request) and total_guests <= (room.max_guests * rooms_request):
                    adults_price = adults * rp.adult

                    # Check how many children
                    all_children = list([first_child if children == 'one' else first_child, second_child])

                    # Check each child of what age is it and add the correct price from the rateplan
                    for child in all_children:

                        if child == '7-12':
                            children_price += rp.child_under_12_exb
                        elif child == '2-6':
                            children_price += rp.child_under_7_exb
                        elif child == '0-2':
                            children_price += rp.child_under_2_exb
            
                if adults < (room.min_guests * rooms_request):
                        # Get the difference Example: 1 adult with 2 children - min guests = 3 - 1 adult == 2, 2 children must be taxed for regular bed
                        adults_difference = (room.min_guests * rooms_request) - adults
                
                        end = adults_difference
                        for child in range(1, adults_difference + (1 if adults_difference == end else 0)):
                            children_price += rp.child_under_12_rb
                            children_on_regular_bed += 1
                              
                            children_extra_bed = (total_children - children_on_regular_bed) * rp.child_under_12_exb
                            #children_price += children_extra_bed

                            adults_price = adults * rp.adult
            
                # If there is rate plan for the selected dates
                if rp and listed_room.listed_date == checkout - timedelta(days=1):

                    price_per_day_room = (adults_price + children_price) / rooms_request
                    price_per_room_all_days = price_per_day_room * rooms_request
                    all_rooms_total = price_per_room_all_days * total_days

                    room_option = {
                        'room_type': room.name,
                        'room_quantity': rooms_request,
                        'from_date': checkin,
                        'to_date': checkout,
                        'total_days': total_days,
                        'total_guests': total_guests,
                        'total_adults': adults,
                        'total_children': total_children,
                        'children_age': tuple([first_child, second_child]) if total_children == 2 else first_child,
                        'price_per_day': price_per_day_room,
                        'price_room_stay': price_per_room_all_days,
                        'total_price': all_rooms_total,
                        'room_image': room.room_image,
                        'room_info': room.room_description

                        }   

                    return room_option