const MAINURL = "https://pcube-marketing.herokuapp.com/";

function preview_image(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById('output_image');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

var posts, companys, company_array;

function clear_filters() {
    var select = document.getElementById("company");
    var length = select.options.length;
    for (i = length - 1; i > 0; i--) {
        select.options[i] = null;
    }
}

function handleChange(src) {
    var y, f = 0;
    Object.keys(companys).forEach(function(key) {
        if (src.value == key) {
            console.log(key);
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



function onPageLoad() {

    var url = MAINURL + "companynames/";
    $.get(url, function(data, status) {
        if (data) {
            companys = data;
            var y = new Array;
            var radios = document.getElementsByClassName('radios')[0];
            Object.keys(companys).forEach(function(key) {

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
