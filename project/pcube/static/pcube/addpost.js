function preview_image(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById('output_image');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

var posts, companys;

function clear_filters() {
    var select = document.getElementById("company");
    var length = select.options.length;
    for (i = length - 1; i >= 0; i--) {
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
    clear_filters()
    filter_companies(y);
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