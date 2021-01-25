function del() {
    var x = document.getElementById("sure");
    x.classList.add("active");
}

function cncl() {
    var x = document.getElementById("sure");
    x.classList.remove("active");
}

function sell(el) {
    // var x = document.getElementsByClassName("msg2")[0];
    // console.log(document.getElementsByClassName("msg2")[0]);
    document.getElementById("del2").value = el.value;
    console.log(el.value);
    $('.msg1').addClass('active');
}

function dell(el) {
    document.getElementById("del").value = el.value;
    console.log(el.value);
    $('.msg2').addClass('active');
}

function cnclsend() {
    $('.msg1').removeClass('active');
}

function cncldel() {
    $('.msg2').removeClass('active');
}


function checkform(ele) {
    var value = ele.getElementsByTagName('input')[1].value;
    var patt1 = /\w/g;
    var variables = value.match(patt1);
    console.log(variables);
    if (variables == null || variables.length < 2) {
        alert('Please enter the valid Text:');
        return false;
    }
    return true;
}