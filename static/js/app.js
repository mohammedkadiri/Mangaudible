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
var play_btn = document.querySelector('.play-btn');
var pause_btn = document.querySelector('.pause-btn');
var x = document.querySelector('#myAudio');
var timer = null;


// play_btn.addEventListener("click", function() {
//     x.play();
// });


// pause_btn.addEventListener("click", function() {
//     x.pause();
// });



// Server data 
var server = "http://127.0.0.1:5000";
var img_data = { 'value': ["text"] };
var img_url = $(".page").attr('src');

// Send a request to server with search entry
search_box.addEventListener('submit', () => {
    var appdir = '/manga/' + search_value.value;
    console.log('appdir')
    search_box.action = appdir;
});


$(document).ready(() => {
    $(document).on('change', '#chapter', function() {
        // Change the chapter option in dropdown menu and update the page content
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
        // Change the page option in dropdown menu and update the page content
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
        // Go back to previous page and update image and dropdown menu
        url = getImageUrl("prev");
        img_url = url;
        page_container.setAttribute('src', url);
        page_num.innerHTML = page.value;
    });

    $(document).on('click', '.next', function() {
        // Go back to next page and update image and dropdown menu
        url = getImageUrl("next");
        img_url = url;
        page_container.setAttribute('src', url);
        page_num.innerHTML = page.value;
    });

    function getImageUrl(x) {
        // Get the current image and display it 
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
        // update the image url
        img_data['value'] = img_url;
    }




    $("#process").click(function() {
        $(".process-data").html(" ");
        var appdir = '/process';
        var send_msg = '<p>Sending image url</p>';
        update();
        console.log(send_msg);

        // Remove the image if a process button is clicked
        if ($(".processed_page").length) {
            $(".processed_page").remove();
        }

        $("#process").toggleClass("progress-bar-clicked");
        $(".progress-bar-striped").css("width", 10 + "%");
        let feedback = document.querySelector("#feedback");
        feedback.textContent = "Processing";

        // Send a post request to server to process a manga page
        $.ajax({
            type: "POST",
            url: server + appdir,
            data: JSON.stringify(img_data),
            dataType: 'json'
        }).done(function(data) {
            // Update the page with a processed page 
            $(".progress-bar-striped").css("width", 100 + "%");
            let img_url = `<img src="data:image/png;base64,${data['msg']}" class="processed_page"style="width:600px;height:800px">`;
            $(".process-data").after(img_url);
            // $(".process-data").html(data['msg']);
            feedback.textContent = "Processed";
            $("#process").toggleClass("progress-bar-clicked");
        });
    });
});