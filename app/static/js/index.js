// nav background
// let header = document.querySelector("header");

// window.addEventListener("scroll", () => {
//     header.classList.toggle("shadow", window.scrollY > 0)
// })
document.addEventListener('DOMContentLoaded', () => {
    const navToggleBtn = document.querySelector('[data-nav-toggle-btn]');
    const navUl = document.querySelector('header nav ul');
    const overlay = document.querySelector('[data-overlay]');
    const featureDropdown = document.querySelector('.dropdown');
    const dropdownButton = featureDropdown.querySelector('.dropbtn');
    const dropdownLinks = document.querySelectorAll('.dropdown-content a');
    const otherNavLinks = document.querySelectorAll('header nav ul li:not(.dropdown) a');
    const closeButton = document.querySelector('.nav-close-btn');

    // Toggle navigation menu and overlay visibility
    navToggleBtn.addEventListener('click', () => {
        navUl.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // Close navigation menu and overlay when overlay is clicked
    overlay.addEventListener('click', () => {
        navUl.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Toggle dropdown content on click for the Feature button
    dropdownButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default link behavior
        featureDropdown.classList.toggle('active');
    });

    // Close dropdown on clicking other navigation items
    otherNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            featureDropdown.classList.remove('active');
            if (window.innerWidth <= 768) {
                navUl.classList.remove('active');
                overlay.classList.remove('active');
            }
        });
    });

    // Close dropdown when clicking on dropdown links
    dropdownLinks.forEach(link => {
        link.addEventListener('click', () => {
            featureDropdown.classList.remove('active');
            if (window.innerWidth <= 768) {
                navUl.classList.remove('active');
                overlay.classList.remove('active');
            }
        });
    });

    // Close mobile navigation menu when clicking on the close button
    closeButton.addEventListener('click', () => {
        navUl.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Close dropdown when clicking outside of it
    document.addEventListener('click', (event) => {
        if (!event.target.closest('.dropdown') && !event.target.closest('[data-nav-toggle-btn]') && !event.target.closest('header')) {
            featureDropdown.classList.remove('active');
        }
    });
});



function toggleAnswer(element) {
    const answer = element.parentElement.querySelector('.faq-answer');
    if (answer.style.display === "block") {
        answer.style.display = "none";
        element.classList.remove("active");
    } else {
        answer.style.display = "block";
        element.classList.add("active");
    }
}

// document.addEventListener('DOMContentLoaded', function () {
//     const monthlyPlans = [
//         {
//             name: 'Basic',
//             price1: '$9.99',
//             features: ['100 Monthly invoice', '25 Save clients', 'Up to 2 team members', 'Estimated (Quotes)']
//         },
//         {
//             name: 'Professional',
//             price1: '$19.99',
//             features: ['250 Monthly invoice', '100 Save clients', 'Up to 10 team members', 'Invoice reminder', 'Recurring statements']
//         },
//         {
//             name: 'Enterprise',
//             price1: '$29.99',
//             features: ['Unlimited monthly invoice', 'Unlimited save clients', 'Up to 25 team members', 'Invoice reminder', 'Recurring statements']
//         }
//     ];

//     const yearlyPlans = [
//         {
//             name: 'Basic',
//             price1: '$99.99',
//             features: ['100 Monthly invoice', '25 Save clients', 'Up to 2 team members', 'Estimated (Quotes)']
//         },
//         {
//             name: 'Professional',
//             price1: '$199.99',
//             features: ['250 Monthly invoice', '100 Save clients', 'Up to 10 team members', 'Invoice reminder', 'Recurring statements']
//         },
//         {
//             name: 'Enterprise',
//             price1: '$299.99',
//             features: ['Unlimited monthly invoice', 'Unlimited save clients', 'Up to 25 team members', 'Invoice reminder', 'Recurring statements']
//         }
//     ];

//     const pricingPlansContainer = document.getElementById('pricing-plans');

//     function renderPlans(plans) {
//         pricingPlansContainer.innerHTML = '';
//         plans.forEach(plan => {
//             const planDiv = document.createElement('div');
//             planDiv.classList.add('plan', plan.name.toLowerCase());

//             planDiv.innerHTML = `
//                 <h2>${plan.name}</h2>
//                 <div class="content">
//                     <p class="price1">${plan.price1}</p>
//                     <p>Free account with limited features.</p>
//                     <ul>
//                         ${plan.features.map(feature => `<li>${feature}</li>`).join('')}
//                     </ul>
//                     <button class="get-started">Get started</button>
//                 </div>
//             `;
//             pricingPlansContainer.appendChild(planDiv);
//         });
//     }

//     document.getElementById('yearly').addEventListener('click', function () {
//         document.querySelector('.toggle .active').classList.remove('active');
//         this.classList.add('active');
//         renderPlans(yearlyPlans);
//     });

//     document.getElementById('monthly').addEventListener('click', function () {
//         document.querySelector('.toggle .active').classList.remove('active');
//         this.classList.add('active');
//         renderPlans(monthlyPlans);
//     });

//     // Initial render
//     renderPlans(monthlyPlans);
// });

// var swiper = new Swiper('.swiper-container', {
//     slidesPerView: 1,
//     spaceBetween: 20,
//     effect: 'fade',
//     loop: true,
//     speed: 300,
//     mousewheel: {
//       invert: false,
//     },
//     pagination: {
//       el: '.swiper-pagination',
//       clickable: true,
//       dynamicBullets: true
//     },
//     // Navigation arrows
//     navigation: {
//       nextEl: '.swiper-button-next',
//       prevEl: '.swiper-button-prev',
//     }
//   });

document.addEventListener('DOMContentLoaded', function () {
    const monthlyPlans = [
        {
            name: 'Basic',
            price1: '$9.99',
            features: ['100 Monthly invoice', '25 Save clients', 'Up to 2 team members', 'Estimated (Quotes)']
        },
        {
            name: 'Professional',
            price1: '$19.99',
            features: ['250 Monthly invoice', '100 Save clients', 'Up to 10 team members', 'Invoice reminder', 'Recurring statements']
        },
        {
            name: 'Enterprise',
            price1: '$29.99',
            features: ['Unlimited monthly invoice', 'Unlimited save clients', 'Up to 25 team members', 'Invoice reminder', 'Recurring statements']
        }
    ];

    const yearlyPlans = [
        {
            name: 'Basic',
            price1: '$99.99',
            features: ['100 Monthly invoice', '25 Save clients', 'Up to 2 team members', 'Estimated (Quotes)']
        },
        {
            name: 'Professional',
            price1: '$199.99',
            features: ['250 Monthly invoice', '100 Save clients', 'Up to 10 team members', 'Invoice reminder', 'Recurring statements']
        },
        {
            name: 'Enterprise',
            price1: '$299.99',
            features: ['Unlimited monthly invoice', 'Unlimited save clients', 'Up to 25 team members', 'Invoice reminder', 'Recurring statements']
        }
    ];

    const pricingPlansContainer = document.getElementById('pricing-plans');

    function renderPlans(plans) {
        pricingPlansContainer.innerHTML = '';
        plans.forEach((plan, index) => {
            const planDiv = document.createElement('div');
            planDiv.classList.add('plan', plan.name.toLowerCase());

            planDiv.innerHTML = `
                <h2>${plan.name}</h2>
                <div class="content">
                    <p class="price1">${plan.price1}</p>
                    <p>Free account with limited features.</p>
                    <ul>
                        ${plan.features.map(feature => `<li>${feature}</li>`).join('')}
                    </ul>
                    <form method="POST" action="/subscribe/${plan.price1.toLowerCase()}/${plan.name.toLowerCase()}">
                        <button type="submit" class="get-started">Get started</button>
                    </form>
                </div>
            `;
            pricingPlansContainer.appendChild(planDiv);
        });
    }

    document.getElementById('yearly').addEventListener('click', function () {
        document.querySelector('.toggle .active').classList.remove('active');
        this.classList.add('active');
        renderPlans(yearlyPlans);
    });

    document.getElementById('monthly').addEventListener('click', function () {
        document.querySelector('.toggle .active').classList.remove('active');
        this.classList.add('active');
        renderPlans(monthlyPlans);
    });

    // Initial render
    renderPlans(monthlyPlans);
});

  var swiper = new Swiper('.swiper-container', {
    // Swiper settings
    loop: true,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    allowTouchMove: false, // Disable touch interactions
    simulateTouch: false, // Disable mouse interactions
  });

