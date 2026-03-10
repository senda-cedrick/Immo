 $(document).ready(function(){
  $('li').on('click', function(){
     $(this).siblings().removeClass("active");
     $(this).addClass("active");
  })
}) 

const list = document.querySelectorAll('.list');
function activeLink(){
   list.forEach((item) =>
   item.classList.remove('active'));
   this.classList.add('active'); 


}
list.forEach((item) =>
item.addEventListener('click', activeLink));

// // const activePage = window.location.pathname;
// // const navLinks = document.querySelectorAll('nav a').forEach(link => {
// // if(link.href.includes(`${activePage}`)) {
// //     link.classList.add('active');
// // }
// // })  

// // $(document).on('click',' li', function(){
// //     $(this).addClass('active')
// // })
// var btncontainer = document.getElementById("navbar");
// var btns = btncontainer.getElementsByClassName("bt");

// for (var i = 0; i<btns.length; i++){
//     btns[i].addEventListener('click', function(){
//         var current = document.getElementsByClassName("active");
//         current[0].className = current[0].className.replace(" active");
//         this.className += " active";
//     })
// }