// var posts = new Array(),
// companys;

$("#filter-search").click(function() {
    $(".filter-box").toggle();
});

function filter() {
    $(".filter-box").toggle();
    clear_divs();
    var company_selected = document.getElementById("company").value;
    var type = document.querySelector('input[name="type"]:checked').value;
    var min_p = parseFloat(document.getElementById("start-rate").value);
    var max_p = parseFloat(document.getElementById("end-rate").value);
    var filtered = new Array();
    // selecting company
    if (company_selected == "all") {
        filtered = posts;
    } else {
        for (var i = 0; i < posts.length; i++) {
            if (posts[i].fields["brand"].toLowerCase() == company_selected)
                filtered.push(posts[i]);
        }
    }

    // selecting type
    var filtered2 = new Array();
    if (type == "all") {
        filtered2 = filtered;
    } else {
        for (var i = 0; i < filtered.length; i++) {
            if (filtered[i].fields["post_type"].toLowerCase() == type)
                filtered2.push(filtered[i]);
        }
    }

    var filtered = new Array();

    if (!isNaN(min_p)) {
        for (var i = 0; i < filtered2.length; i++) {
            if (filtered2[i].fields["newprice"] >= min_p)
                filtered.push(filtered2[i]);
        }
    } else {
        for (var i = 0; i < filtered2.length; i++) {
            filtered.push(filtered2[i]);
        }
    }


    var filtered2 = new Array();
    if (!isNaN(max_p)) {
        for (var i = 0; i < filtered.length; i++) {
            if (filtered[i].fields["newprice"] <= max_p) {
                filtered2.push(filtered[i]);
            }
        }
    } else {
        for (var i = 0; i < filtered.length; i++) {
            filtered2.push(filtered[i]);
        }
    }
    display(filtered2);
}

function clear_divs() {
    document.getElementsByClassName("box-container")[0].innerHTML = "";
}

function clear_filters() {
    var select = document.getElementById("company");
    var length = select.options.length;
    for (i = length - 1; i > 0; i--) {
        select.options[i] = null;
    }
}

function handleChange(src) {
    if (src.value == "fashion")
        var y = companys["fashion"];
    else if (src.value == "electronics")
        var y = companys["electronic"];
    else if (src.value == "mobiles")
        var y = companys["mobile"];
    else {
        var y = companys["fashion"].concat(companys["electronic"]);
        y = y.concat(companys["mobile"]);
    }
    clear_filters()
    filter_companies(y);
}


function display(selected_posts) {
    var i;
    for (i = selected_posts.length - 1; i >= 0; i--) {
        // console.log(posts[i].fields);
        // $('.box-container').append('<div class="card"><div class="imgBx"><img src="http://127.0.0.1:8000/media/' + selected_posts[i].fields.image + '"></div><div class="contentBx"><hr style="width:100%"><h1>' + selected_posts[i].fields.title + '</h1><h5>' + selected_posts[i].fields.brand + '</h5><h2 class="price">&#8377;' + selected_posts[i].fields.newprice + '</h2><a href="http://127.0.0.1:8000/post/' + selected_posts[i].pk + '" class="buy">More Info</a></div></div>');
        $('.box-container').append('<div class="product"><p class="product-title">' + selected_posts[i].fields.title + '</p><img src="http://127.0.0.1:8000/media/' + selected_posts[i].fields.image + '" alt="image" /><div class="product-text"><p class="brand">' + selected_posts[i].fields.brand + '</p><h3>&#8377;' + selected_posts[i].fields.newprice + '</h3><button><a href="http://127.0.0.1:8000/post/' + selected_posts[i].pk + '">View Product</a></button></div></div>');
    }
}

function filter_companies(y) {
    y.sort();
    select = document.getElementById('company');
    // console.log(y);
    for (var i = 0; i < y.length; i++) {
        var opt = document.createElement('option');
        opt.value = y[i];
        opt.innerHTML = y[i];
        select.appendChild(opt);
    }
}

function onPageLoad() {

    $(".filter-box").toggle();
    display(posts);

    var url = "http://127.0.0.1:8000/companynames/";
    $.get(url, function(data, status) {
        // console.log("got response for allpost request");
        if (data) {
            companys = data;
            var y = companys["fashion"].concat(companys["electronic"]);
            y = y.concat(companys["mobile"]);
            filter_companies(y);
        }
    });
}

window.onload = onPageLoad;