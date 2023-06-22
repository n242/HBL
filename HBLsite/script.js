// Function to check if an element is in the viewport
function isElementInViewport(element) {
    var rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }
  
  // Function to handle the intersection changes
  function handleIntersection(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
      } else {
        entry.target.classList.remove('fade-in');
      }
    });
  }
  
  // Create a new Intersection Observer instance
  var observer = new IntersectionObserver(handleIntersection);
  
  // Get all the sections
  var sections = document.querySelectorAll('section');
  
  // Observe each section
  sections.forEach(function(section) {
    observer.observe(section);
  });
  
  // Function to handle the scroll event
  function handleScroll() {
    sections.forEach(function(section) {
      if (isElementInViewport(section) && !section.classList.contains('fade-in')) {
        section.classList.add('fade-in');
      } else if (!isElementInViewport(section) && section.classList.contains('fade-in')) {
        section.classList.remove('fade-in');
      }
    });
  }
  
  // Add scroll event listener
  window.addEventListener('scroll', handleScroll);
  