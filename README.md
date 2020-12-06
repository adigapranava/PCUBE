# PCUBE
Profile:
   [ user, fullname, phoneno, address, state, city, image]
    
    
Post:
    [ title, brand, discription, date_posted, address, state, city, phone, oldprice, newprice, owner, image]
    
#### API FOR ALL POSTS ####
var url = "http://127.0.0.1:8000/allposts/";
    $.get(url,function(data, status) {
        console.log("got response for give_details request");
        if(data) {
            console.log( data );
        }
    });
    

#TODO: Comments Likes Buy
