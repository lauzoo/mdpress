function saveAs(title, content)
{
    var contentTemplate =	'<!DOCTYPE html>' +
        '<html lang="zh">' +
        '<head>' +
        '	<meta charset="utf-8" />' +
        '	<title>{{{ title }}}</title>' +
        '    <link rel="stylesheet" href="css/style.css" />' +
        '    <link rel="stylesheet" href="css/editormd.css" />' +
        '</head>' +
        '<body>' +
        '  <div id="content">' +
        '{{{ content }}}' +
        '	</div>' +
        '</body>' ;
    var templateFunction = Handlebars.compile(contentTemplate);
    var data = {"title": title, "content": content};
    var result = templateFunction(data);

    if (name === null)
    {
        name = dt.getFullYear() + "-" + (dt.getMonth() + 1) + "-" + dt.getDate() + "-" + dt.getTime() + ".html";
    }

    req_data = JSON.stringify({
        'name': name,
        'content': result,
    })
    $.ajax({
      url: "/posts/post",
      type: "POST",
      headers: {
        "Authorization": "JWT " + jwt_token,
      },
      contentType: 'application/json',
      data: req_data,
      success: function(){
          alert("Save Success");
      }
    });
}

function listAll()
{
    window.location.href = "/posts/all";
}


function openLogin() {
  editor.htmlEntitiesDialog();
}
