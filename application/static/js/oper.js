function listAll()
{
    window.location.href = "/posts/all";
}


function openLogin() {
  editor.htmlEntitiesDialog();
}

function save_post() {
  title = $("#title").val();
  slug = $("#slug").val();
  markdown = editor.getMarkdown();
  html = editor.getPreviewedHTML();
  categories = $("#category").val();
  status = $("#post-state").val();
  postdate= $("#post-date").val();

  req_data = JSON.stringify({
    title: title, slug: slug, content: markdown,
    categories: categories, status: status,
    tags: []
  })
  console.log(localStorage.twtf_jwt_token);
  $.ajax({
    url: "/posts/post",
    type: "POST",
    headers: {
      "Authorization": "Bearer " + localStorage.twtf_jwt_token,
    },
    contentType: 'application/json',
    data: req_data,
    success: function(data){
      if (data.code != 2000) {
        console.log(data);
      } else {
        alert('save success!');
      }
    }
  });
  return false;
}
