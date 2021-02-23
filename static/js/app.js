// Get value from select 
var chapter = document.querySelector('#chapter');
var chapter_num = document.querySelector('.chapter-num');
var page_num = document.querySelector('.page-num');
var page = document.querySelector('#pager');
var manga_name = document.querySelector('.current').innerHTML;
var page_container = document.querySelector('.page');
var url  = "https://storage.cloud.google.com/mangaudible/manga/"
var prev = document.querySelector('.prev');
var next = document.querySelector('.next');
var lastValue = page.options[page.options.length - 1].value;


chapter.addEventListener('change', function() {
    url  = "https://storage.cloud.google.com/mangaudible/manga/"
   let chapter_value = chapter.options[chapter.selectedIndex].value;
   let page_value = page.options[pager.selectedIndex].value;
   manga_name = manga_name.replace( /\s/g, "%20");
   url += manga_name + "/" + chapter_value + "/" + page.value + ".jpg";
   chapter_num.innerHTML = this.options[this.selectedIndex].text;
   page_container.setAttribute('src', url);
});


page.addEventListener('change', function() {
    url  = "https://storage.cloud.google.com/mangaudible/manga/"
   let chapter_value = chapter.options[chapter.selectedIndex].value;
   let page_value = page.options[pager.selectedIndex].value;
   manga_name = manga_name.replace( /\s/g, "%20");
   url += manga_name + "/" + chapter_value + "/" + page.value + ".jpg";
   chapter_num.innerHTML = this.options[this.selectedIndex].text;
   page_num.innerHTML = page.value;
   page_container.setAttribute('src', url);
});


prev.addEventListener('click', () => {
    url = getImageUrl("prev");
    page_container.setAttribute('src', url);
    page_num.innerHTML = page.value;
})

next.addEventListener('click', () => {
    url = getImageUrl("next");
    page_container.setAttribute('src', url);
    page_num.innerHTML = page.value;
})


function getImageUrl(x) {
    url  = "https://storage.cloud.google.com/mangaudible/manga/"
    let chapter_value = chapter.options[chapter.selectedIndex].value;
    let page_value = page.options[pager.selectedIndex].value;
    manga_name = manga_name.replace( /\s/g, "%20");
    page_value = parseInt(page_value);

    if(x === 'next')
    {
        if(page_value + 1 > lastValue)
            url += manga_name + "/" + chapter_value + "/" + page_value + ".jpg";
        else {
            let newValue = parseInt(page_value + 1);
            page.value = newValue.toString();
            url += manga_name + "/" + chapter_value + "/" + newValue + ".jpg";  
        }
               
    }
    if(x === "prev"){
        if(page_value - 1 == 0)
            url += manga_name + "/" + chapter_value + "/" + page_value + ".jpg";
        else {
            let newValue = parseInt(page_value - 1);
            page.value = newValue.toString();
            url += manga_name + "/" + chapter_value + "/" + newValue + ".jpg";
        }
            
    }
    return url;
}
