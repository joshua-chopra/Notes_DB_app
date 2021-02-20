function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    // bring us back to the same page
    window.location.href = "/";
  });
}

function redirect_google() {
  const search_params = document.getElementById('input').value;
  window.location.href('https://www.google.com/search?q=' + search_params);
}