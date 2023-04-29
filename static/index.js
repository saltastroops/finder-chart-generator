const tabs = [...document.querySelectorAll("#form-tabs li")];

const tabContainer = document.querySelector("#tab-content");

const tabContents = [...document.querySelectorAll("#tab-content > div")].reduce(
        (prev, content, i) => ({...prev, [content.id]: content}), {});

const fitsFileOptionElements = {
  image_survey_element: document.querySelector("#image_survey_element"),
  custom_fits_element: document.querySelector("#custom_fits_element")
}

const data = {}
const errors = {}


function switchTab(event) {
  // Store the form data
  const form = document.querySelector("form");
  const formData = new FormData(form);
  for (let e of formData.entries()) {
    data[e[0]] = e[1];
  }

  // Select the tab the user clicked on
  selectTab(event.currentTarget);

  // Apply the previously saved form data
  const inputElements = document.querySelectorAll(`input`);
  for (let inputElement of inputElements) {
    const name = inputElement.getAttribute("name");
    const inputType = inputElement.getAttribute("type")
    if (data[name] && ["text", "", null].includes(inputType)) {
      inputElement.value = data[name];
    }
  }
}

function selectTab(selectedTab) {
  // Unselect all tabs
  tabs.forEach(tab => tab.classList.remove("is-active"));

  // Select the given tab
  selectedTab.classList.add("is-active");

  // Display the content of the selected tab
  displayTabContent(selectedTab);
}

function displayTabContent(selectedTab) {
  // Hide all the tab content
  tabContainer.innerHTML = "";

  // show the content of the selected tab
  const target = selectedTab.dataset.target;
  tabContainer.appendChild(tabContents[target]);
}

function switchFitsOption(event) {
  // Get the id of the FITS file option element from the data-target attribute value
  // of the selected radio button.
  const targetId = event.target.dataset.target;

  // Select the FITS option element
  selectFitsOption(targetId);
}

function selectFitsOption(optionElementId) {
  // Clear any previous selection
  const optionElementContainer = document.querySelector("#fits_option");
  optionElementContainer.innerHTML = "";

  // Add the selected FITS file option element
  optionElementContainer.appendChild(fitsFileOptionElements[optionElementId])
}

async function generateFinderChart(event) {
  event.preventDefault();
  const selectedTab = tabs.find(tab => tab.classList.contains("is-active"));
  const target = selectedTab.dataset.target;
  const mode = target.split("_form")[0];
  const url = `/finder-charts?mode=${mode}`;
  const formData = new FormData(event.target);
  const response = await fetch(url, { method: "POST", body: formData });
  console.log(mode, await response.json())
}

function init() {
  // Add an event listener to all the tabs
  tabs.forEach(tab => tab.addEventListener("click", switchTab));

  // Add an event listener to the radio buttons for selecting the FITS file option
  document.querySelectorAll("#fits_controls input")
          .forEach(input => input.addEventListener("click", switchFitsOption));

  // Add the event listener for generating the finder chart
  document.querySelector("form").addEventListener("submit", generateFinderChart);

  // Select the first tab
  selectTab(tabs[0]);

  // Select image survey as the FITS file option
  selectFitsOption("image_survey_element");
}

init();
