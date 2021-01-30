var rad = document.getElementsByName('option')

function changed(x) {
    show((x.id).substring(0, (x.id).length - 2));
}

function show(name) {
    ass = document.getElementsByClassName('my-list')[0];
    dec = ass.getElementsByClassName('options_div');
    var i;
    for (i = 0; i < dec.length; i++) {
        if (dec[i].id == name) {
            dec[i].style.display = 'block';
        } else {
            dec[i].style.display = 'none';
        }
    }
}

function onPageLoad() {
    var i;
    for (i = 0; i < rad.length; i++) {
        if (rad[i].checked) {
            var x = (rad[i].id).substring(0, (rad[i].id).length - 2);
            show(x);
        }
    }

}

window.onload = onPageLoad;