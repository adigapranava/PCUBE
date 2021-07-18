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

-----------------------------------------------------------
#TO GIT:
Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
-------
1)Go to folder
2)git init
3)git add <project_name>
4)git commit -m "<message>"
5)git push -u origin master
