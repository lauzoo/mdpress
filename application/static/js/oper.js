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

    $.ajax({
      url: "/post",
      type: "POST",
      headers: {
        "Authorization": "JWT",
      },
      data: {
          'name': name,
          'content': result
      },
      success: function(){
          alert("Save Success");
      }
    });
}

function listAll()
{
    window.location.href = "/post";
}
