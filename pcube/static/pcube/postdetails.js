const MAINURL = "https://pcube-marketing.herokuapp.com/post/";

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
    console.log("variables");
    if (variables == null || variables.length < 2) {
        alert('Please enter the valid Text:');
        return false;
    }
    return true;
}



// Copy link

function myFunction(item, ques) {
    var text = MAINURL + item + "/#question-no-" + ques;
    copyText(text);
}

function myFunction2(item) {
    var text = MAINURL + item;
    copyText(text);
}

function copyText(text) {
    var temp = document.createElement('input');
    temp.value = text;
    var body = document.getElementsByTagName('body')[0];
    body.appendChild(temp);
    temp.select();
    temp.setSelectionRange(0, 99999);
    document.execCommand("copy");
    temp.remove();

    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Link Copied: ";
    var tooltip2 = document.getElementById("myTooltip2");
    tooltip2.innerHTML = "Link Copied: ";
}

function outFunc() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy Link to clipboard";
}