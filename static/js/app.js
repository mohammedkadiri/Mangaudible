// Get value from select 
let chapter = document.querySelector('#chapter');
let page = document.querySelector('#pager');
let manga_name = document.querySelector('.current');
let page_container = document.querySelector('.page');
var url  = "https://storage.cloud.google.com/mangaudible/manga/"


chapter.addEventListener('change', function() {
    url  = "https://storage.cloud.google.com/mangaudible/manga/"
   let chapter_value = chapter.options[chapter.selectedIndex].value;
   let page_value = page.options[pager.selectedIndex].value;
   // let text = chapter.options[chapter.selectedIndex].text;
   manga_name = manga_name.replace(/ /g, "%20");
   url += manga_name + "/" + chapter_value + "/" + page.value + ".jpg";
   console.log(url);
   page_container.setAttribute('src', url);

   // page.setAttribute('src', value);
});


page.addEventListener('change', function() {
    url  = "https://storage.cloud.google.com/mangaudible/manga/"
   let chapter_value = chapter.options[chapter.selectedIndex].value;
   let page_value = page.options[pager.selectedIndex].value;
   // let text = chapter.options[chapter.selectedIndex].text;
   manga_name = manga_name.replace(/ /g, "%20");
   url += manga_name + "/" + chapter_value + "/" + page.value + ".jpg";
   console.log(url);
   page_container.setAttribute('src', url);
});