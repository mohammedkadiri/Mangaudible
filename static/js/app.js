// Get value from select 
var chapter = document.querySelector('#chapter');
var chapter_num = document.querySelector('.chapter-num');
var page_num = document.querySelector('.page-num');
var page = document.querySelector('#pager');
var manga_name = document.querySelector('.current');
var page_container = document.querySelector('.page');
var url = "https://storage.cloud.google.com/mangaudible/manga/"
var prev = document.querySelector('.prev');
var next = document.querySelector('.next');
var search_box = document.querySelector('#search-box');
var search_value = document.querySelector('.form-control');
var timer = null;





// Server data 
var server = "http://127.0.0.1:5000";
var img_data = { 'value': ["text"] };
var img_url = $(".page").attr('src');


search_box.addEventListener('submit', () => {
    var appdir = '/manga/' + search_value.value;
    search_box.action = appdir;
});


$(document).ready(() => {
    $(document).on('change', '#chapter', function() {
        url = "https://storage.cloud.google.com/mangaudible/manga/"
        let chapter_value = chapter.options[chapter.selectedIndex].value;
        let page_value = page.options[pager.selectedIndex].value;
        manga_name.innerHTML = manga_name.innerHTML.replace(/\s/g, "%20");
        url += manga_name.innerHTML + "/" + chapter_value + "/" + page.value + ".jpg";
        chapter_num.innerHTML = this.options[this.selectedIndex].text;
        page_container.setAttribute('src', url);
        img_url = url;
    });

    $(document).on('change', '#pager', function() {
        url = "https://storage.cloud.google.com/mangaudible/manga/"
        let chapter_value = chapter.options[chapter.selectedIndex].value;
        let page_value = page.options[pager.selectedIndex].value;
        manga_name.innerHTML = manga_name.innerHTML.replace(/\s/g, "%20");
        url += manga_name.innerHTML + "/" + chapter_value + "/" + page.value + ".jpg";
        chapter_num.innerHTML = this.options[this.selectedIndex].text;
        page_num.innerHTML = page.value;
        page_container.setAttribute('src', url);
        img_url = url;
    });


    $(document).on('click', '.prev', function() {
        url = getImageUrl("prev");
        img_url = url;
        page_container.setAttribute('src', url);
        page_num.innerHTML = page.value;
    });

    $(document).on('click', '.next', function() {
        url = getImageUrl("next");
        img_url = url;
        page_container.setAttribute('src', url);
        page_num.innerHTML = page.value;
    });

    function getImageUrl(x) {
        url = "https://storage.cloud.google.com/mangaudible/manga/"
        let chapter_value = chapter.options[chapter.selectedIndex].value;
        let page_value = page.options[pager.selectedIndex].value;
        manga_name.innerHTML = manga_name.innerHTML.replace(/\s/g, "%20");
        page_value = parseInt(page_value);

        if (x === 'next') {
            if (page_value + 1 > page.options[page.options.length - 1].value)
                url += manga_name.innerHTML + "/" + chapter_value + "/" + page_value + ".jpg";
            else {
                let newValue = parseInt(page_value + 1);
                page.value = newValue.toString();
                url += manga_name.innerHTML + "/" + chapter_value + "/" + newValue + ".jpg";
            }

        }
        if (x === "prev") {
            if (page_value - 1 == 0)
                url += manga_name.innerHTML + "/" + chapter_value + "/" + page_value + ".jpg";
            else {
                let newValue = parseInt(page_value - 1);
                page.value = newValue.toString();
                url += manga_name.innerHTML + "/" + chapter_value + "/" + newValue + ".jpg";
            }

        }
        return url;
    }


    function update() {
        img_data['value'] = img_url;
    }




    $("#process").click(function() {
        $(".process-data").html(" ");
        var appdir = '/process';
        var send_msg = '<p>Sending image url</p>';
        update();
        console.log(send_msg);

        $("#process").toggleClass("progress-bar-clicked");
        $(".progress-bar-striped").css("width", 10 + "%");
        let feedback = document.querySelector("#feedback");
        feedback.textContent = "Processing";

        $.ajax({
            type: "POST",
            url: server + appdir,
            data: JSON.stringify(img_data),
            dataType: 'json'
        }).done(function(data) {
            console.log(data);
            $(".progress-bar-striped").css("width", 100 + "%");
            $(".process-data").html(data['msg']);
            feedback.textContent = "Processed";
            $("#process").toggleClass("progress-bar-clicked");
        });



    });
});