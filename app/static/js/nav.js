const toggleButton = document.getElementsByClassName("toggle-button");

let addEv = function () {
  const navbarLinks = document.getElementsByClassName("top-nav-links")[0];
  toggleButton[0].addEventListener("click", () => {
    navbarLinks.classList.toggle("active");
  });
};

function resolve() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(addEv());
    }, 500);
  });
}

async function asyncCall() {
  const result = await resolve();
}

asyncCall();
