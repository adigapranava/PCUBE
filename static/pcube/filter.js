var posts, companys, MAINURL, company_array;

MAINURL = window.location.href;
MAINURL = MAINURL.split('#')[0];

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

/////remove the
function clear_filters() {
    var select = document.getElementById("company");
    var length = select.options.length;
    for (i = length - 1; i > 0; i--) {
        select.options[i] = null;
    }
}

/////handel the change in radio buttons
function handleChange(src) {
    var y, f = 0;
    Object.keys(companys).forEach(function(key) {
        if (src.value == key) {
            y = companys[key];
            f = 1;
        }
    });
    if (f == 0) {
        y = company_array;
    }
    clear_filters()
    filter_companies(y);
}

// //// display the selected posts
function display(selected_posts) {
    var i;
    for (i = selected_posts.length - 1; i >= 0; i--) {
        if (!selected_posts[i].fields.sold)
            $('.box-container').append('<div class="product"><p class="product-title">' +
                selected_posts[i].fields.title +
                '</p><img src="' + MAINURL + 'media/' +
                selected_posts[i].fields.image +
                '" alt="image" /><div class="product-text"><p class="brand">' +
                selected_posts[i].fields.brand +
                '</p><h3>&#8377;' +
                selected_posts[i].fields.newprice +
                '</h3><a href="' + MAINURL + 'post/' +
                selected_posts[i].pk +
                '"><button>View Product</button></a></div></div>');
    }
}

// add companys to dropdown by filtering
function filter_companies(y) {
    // remove duplicates from array
    y = y.filter(function(item, pos) {
        return y.indexOf(item) == pos;
    })
    y.sort();

    select = document.getElementById('company');
    for (var i = 0; i < y.length; i++) {
        var opt = document.createElement('option');
        opt.value = y[i];
        opt.innerHTML = y[i];
        select.appendChild(opt);
    }
}

//////search the products;
var form = document.getElementById('form');
form.addEventListener('submit', function(e) {
    e.preventDefault();
    var query = "";
    query = document.getElementById('id_q_large').value;
    if (query == "" || query == " ") {
        clear_divs();
        display(posts);
    } else {
        var url = MAINURL + "search/?q=" + query;
        $.get(url, function(data, status) {
            if (data) {
                clear_divs();
                display(data);
            }
        });
    }
});

////ON PAGE LOADERS
function onPageLoad() {

    $(".filter-box").toggle();

    // get all posts details
    var url = MAINURL + "allposts/";
    $.get(url, function(data, status) {
        if (data) {
            posts = data;
            display(posts);
        }
    });

    // get all brands details
    var url = MAINURL + "companynames/";
    $.get(url, function(data, status) {
        if (data) {
            companys = data;
            var y = new Array;
            var radios = document.getElementsByClassName('radios')[0];
            Object.keys(companys).forEach(function(key) {
                // create a radio buttons;
                var rad = document.createElement("input");
                rad.type = "radio";
                rad.value = key;
                rad.id = key;
                rad.name = "type";
                rad.onclick = function() {
                    handleChange(this)
                };

                var label = document.createElement("label");
                label.htmlFor = key;
                label.innerText = key;

                radios.appendChild(rad);
                radios.appendChild(label);

                // array
                var value = companys[key];
                y = y.concat(value);
            });
            company_array = y;
            filter_companies(y);
        }
    });
}

window.onload = onPageLoad;