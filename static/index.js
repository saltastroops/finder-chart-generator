const tabs = document.querySelectorAll("#form-tabs li");

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

function init() {
  // Add an event listener to all the tabs
  tabs.forEach(tab => tab.addEventListener("click", switchTab));

  // Select the first tab
  selectTab(tabs[0]);
}

init();
