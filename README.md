# PCUBE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length= 30, blank=True, null=True)
    phoneno = models.CharField(max_length= 13, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length= 20, blank=True, null=True)
    city = models.CharField(max_length= 20, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', height_field=None)
    
    
class Post(models.Model):
    title = models.CharField(max_length= 30)
    brand = models.CharField(max_length= 20)
    discription = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length= 60)
    state = models.CharField(max_length= 20)
    city = models.CharField(max_length= 20)
    phone = models.CharField(max_length= 15)
    oldprice = models.PositiveIntegerField()
    newprice = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='placeholder.jpg', upload_to='Posts', height_field=None)
    
#### API FOR ALL POSTS ####
var url = "http://127.0.0.1:8000/allposts/";
    $.get(url,function(data, status) {
        console.log("got response for give_details request");
        if(data) {
            console.log( data );
        }
    });
    

#TODO: Comments Likes Buy
