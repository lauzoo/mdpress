function listAll()
{
    window.location.href = "/posts/all";
}


function openLogin() {
    window.location.href = "/admin/login";
}

function save_post() {
    title = $("#title").val();
    slug = $("#slug").val();
    markdown = editor.getMarkdown();
    html = editor.getPreviewedHTML();
    categories = $("#category").val();
    status = $("#post-state").val();
    postdate= $("#post-date").val();

    if (categories === null) {
      categories = [];
    }
    req_data = JSON.stringify({
      title: title, slug: slug, markdown: markdown,
      categories: categories, status: status,
      tags: []
    });

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
};


function load_post(pid) {
  $.ajax({
    url: "/posts/post?id=" + pid,
    type: "GET",
    success: function(data){
      if (data.code != 2000) {
        console.log(data);
      } else {
        post = data.data.post;
        console.log(post);
        editor.setMarkdown(post.markdown);
        categories = post.categories;
        cate_ids = []
        $.each(categories, function(key, value) {
           console.log(key + ":" + value.name);
           cate_ids.push(value.id);
        });
        console.log('categoriest ids' + cate_ids);
        $("#category").val(cate_ids);
        $("#post-status").val(post.status);
        console.log('load post success!');
      }
    }
  });
};


function load_categories() {
  $.ajax({
    url: "/posts/all_categories",
    type: "GET",
    success: function(data){
      console.log("categories");
      console.log(data);
      if (data.code != 2000) {
        console.log(data);
      } else {
        cates = data.data.categories;
        $.each(cates, function(key, value) {
             $('#category')
                 .append($("<option></option>")
                              .attr("value",value.id)
                              .text(value.name));
        });
        console.log('load categories success!');
        if (post_id !== null) {
          console.log('load post!');
          load_post(post_id);
        }
      }
    }
  });
}
