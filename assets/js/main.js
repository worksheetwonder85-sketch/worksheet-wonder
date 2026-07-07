/*==================================================
  Worksheet Wonder
  Main JavaScript File
==================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initializeCounter();

    initializeBackToTop();

    initializeSmoothScroll();

    initializeNavbar();

    initializeNewsletter();

    initializeSearch();

});


/*==================================================
  Animated Counter
==================================================*/

function initializeCounter(){

    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter=>{

        const target = Number(counter.dataset.target);

        let count = 0;

        const speed = target/150;

        const updateCounter = ()=>{

            count += speed;

            if(count < target){

                counter.innerText = Math.floor(count);

                requestAnimationFrame(updateCounter);

            }else{

                counter.innerText = target.toLocaleString();

            }

        };

        updateCounter();

    });

}


/*==================================================
  Back To Top Button
==================================================*/

function initializeBackToTop(){

    const button = document.getElementById("backToTop");

    if(!button) return;

    window.addEventListener("scroll",()=>{

        if(window.scrollY > 400){

            button.style.display="flex";

        }

        else{

            button.style.display="none";

        }

    });

    button.addEventListener("click",()=>{

        window.scrollTo({

            top:0,

            behavior:"smooth"

        });

    });

}


/*==================================================
  Smooth Anchor Scrolling
==================================================*/

function initializeSmoothScroll(){

    document.querySelectorAll('a[href^="#"]').forEach(anchor=>{

        anchor.addEventListener("click",function(e){

            const target=document.querySelector(this.getAttribute("href"));

            if(!target) return;

            e.preventDefault();

            target.scrollIntoView({

                behavior:"smooth",

                block:"start"

            });

        });

    });

}


/*==================================================
  Navbar Shadow
==================================================*/

function initializeNavbar(){

    const navbar=document.querySelector(".navbar");

    if(!navbar) return;

    window.addEventListener("scroll",()=>{

        if(window.scrollY>30){

            navbar.style.boxShadow="0 10px 30px rgba(0,0,0,.10)";

            navbar.style.padding="10px 0";

        }

        else{

            navbar.style.boxShadow="0 4px 20px rgba(0,0,0,.05)";

            navbar.style.padding="14px 0";

        }

    });

}


/*==================================================
  Newsletter Form
==================================================*/

function initializeNewsletter(){

    const form=document.querySelector(".newsletter-section form");

    if(!form) return;

    form.addEventListener("submit",(e)=>{

        e.preventDefault();

        const email=form.querySelector("input");

        if(email.value===""){

            alert("Please enter your email address.");

            email.focus();

            return;

        }

        alert("🎉 Thank you for subscribing!");

        form.reset();

    });

}


/*==================================================
  Search Box
==================================================*/

function initializeSearch(){

    const search=document.querySelector(".hero-search input");

    if(!search) return;

    search.addEventListener("keypress",(e)=>{

        if(e.key==="Enter"){

            e.preventDefault();

            alert("Search feature will be connected in the next version.");

        }

    });

}
/*==================================================
  Worksheet Wonder
  Additional JavaScript
==================================================*/


/*=============================================
  Loader
=============================================*/

window.addEventListener("load", () => {

    const loader = document.querySelector(".loader");

    if(loader){

        loader.classList.add("hidden");

    }

});


/*=============================================
  Reveal Cards on Scroll
=============================================*/

const revealItems = document.querySelectorAll(
".category-card,.worksheet-card,.product-card,.blog-card,.testimonial-card,.feature-box"
);

const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.style.opacity="1";

            entry.target.style.transform="translateY(0)";

        }

    });

},{
    threshold:0.2
});

revealItems.forEach(item=>{

    item.style.opacity="0";

    item.style.transform="translateY(40px)";

    item.style.transition="all .8s ease";

    observer.observe(item);

});


/*=============================================
  Active Navigation Link
=============================================*/

const currentPage = window.location.pathname.split("/").pop();

document.querySelectorAll(".navbar-nav .nav-link").forEach(link=>{

    const href = link.getAttribute("href");

    if(href === currentPage){

        link.classList.add("active");

    }

});


/*=============================================
  Hero Button Ripple Effect
=============================================*/

document.querySelectorAll(".btn").forEach(button=>{

    button.addEventListener("click",function(e){

        const ripple=document.createElement("span");

        ripple.className="ripple";

        const rect=this.getBoundingClientRect();

        ripple.style.left=(e.clientX-rect.left)+"px";

        ripple.style.top=(e.clientY-rect.top)+"px";

        this.appendChild(ripple);

        setTimeout(()=>{

            ripple.remove();

        },600);

    });

});


/*=============================================
  Image Lazy Loading
=============================================*/

document.querySelectorAll("img").forEach(img=>{

    img.loading="lazy";

});


/*=============================================
  Console Welcome
=============================================*/

console.log("%c🌈 Welcome to Worksheet Wonder",
"font-size:22px;color:#4F46E5;font-weight:bold");

console.log("%cMade with ❤️ using HTML, CSS, Bootstrap & JavaScript",
"font-size:14px;color:#06B6D4");


/*=============================================
  Future Features Placeholder
=============================================*/

// Shopping Cart

// Wishlist

// Login Authentication

// PDF Downloads

// Payment Gateway

// Admin Dashboard

// Product Search

// Filters

// Stripe

// Razorpay

// Firebase

// Supabase

// Analytics

// Dark Mode

// AI Worksheet Generator


/*=============================================
  End of File
=============================================*/