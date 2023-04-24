const tabs = document.querySelectorAll("#form-tabs li");

const fitsFileOptionElements = {
  image_survey_element: document.querySelector("#image_survey_element"),
  custom_fits_element: document.querySelector("#custom_fits_element")
}

function switchTab(event) {
  // Select the tab the user clicked on
  selectTab(event.currentTarget);
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
  document.querySelectorAll("#tab-content > div").forEach(e => e.classList.add("is-hidden"));

  // show the content of the selected tab
  const target = selectedTab.dataset.target;
  document.getElementById(target).classList.remove("is-hidden");
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

function init() {
  // Add an event listener to all the tabs
  tabs.forEach(tab => tab.addEventListener("click", switchTab));

  // Add an event listener to the radio buttons for selecting the FITS file option
  document.querySelectorAll("#fits_controls input")
          .forEach(input => input.addEventListener("click", switchFitsOption));

  // Select the first tab
  selectTab(tabs[0]);

  // Select image survey as the FITS file option
  selectFitsOption("image_survey_element");
}

init();
